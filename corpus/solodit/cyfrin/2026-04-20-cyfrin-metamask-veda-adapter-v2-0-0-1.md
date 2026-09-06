---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-20-cyfrin-metamask-veda-adapter-v2-0-0-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-04-20T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-20-cyfrin-metamask-veda-adapter-v2.0.md
tags:
- firm:cyfrin
- report:2026-04-20-cyfrin-metamask-veda-adapter-v2-0
title: Public batch execution is economically griefable because a single pre-consumed
  delegation reverts the entire batch
vuln_class: []
---

# Public batch execution is economically griefable because a single pre-consumed delegation reverts the entire batch

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-20-cyfrin-metamask-veda-adapter-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-20-cyfrin-metamask-veda-adapter-v2.0.md)_

---

**Description:** `VedaAdapter::depositByDelegationBatch` and `VedaAdapter::withdrawByDelegationBatch` process streams sequentially and revert the full transaction if any one stream fails:

```solidity
// VedaAdapter.sol:213-227
function depositByDelegationBatch(DepositParams[] memory _depositStreams) external {
    uint256 streamsLength_ = _depositStreams.length;
    if (streamsLength_ == 0) revert InvalidBatchLength();

    address caller_ = msg.sender;
    for (uint256 i = 0; i < streamsLength_;) {
        DepositParams memory params_ = _depositStreams[i];
        // @audit — if this reverts for ANY stream, the entire batch reverts
        _executeDepositByDelegation(params_.delegations, params_.minimumMint, caller_);
        unchecked {
            ++i;
        }
    }

    emit BatchDepositExecuted(caller_, streamsLength_);
}
```

The same pattern exists in `VedaAdapter::withdrawByDelegationBatch`.

Since `VedaAdapter::depositByDelegation` and `VedaAdapter::withdrawByDelegation` are callable by anyone and delegation chains are visible in the public mempool, an attacker can:

1. Monitor the mempool for a pending batch transaction
2. Extract a single delegation chain from the batch calldata
3. Front-run with a single `depositByDelegation` (or `withdrawByDelegation`) call using that delegation
4. The front-run tx succeeds — the delegation is consumed (enforcer `spentMap` exhausted), and the user receives their shares/assets
5. The operator's batch tx arrives — all streams execute until the consumed delegation reverts, reverting the entire batch

This makes public batching economically fragile. A batch can be invalidated by paying for only one execution, while the operator bears the cost of the reverted aggregate call.

**Impact:** This is an operational denial-of-service / reliability issue against public batching.

- Attackers cannot steal user funds
- Attackers can repeatedly force reverted public batches at materially lower cost than the operator's aggregate execution
- Under sustained mempool griefing, batching may become uneconomic unless the operator switches to private orderflow or to a batch design that tolerates per-stream failure

The practical severity depends on whether the protocol expects these batch entrypoints to be usable on the public mempool. If yes, this issue meaningfully degrades that design goal.

**Proof of Concept:** Add the following test to `VedaLending.t.sol`:

```solidity
    /// @notice Demonstrates batch griefing: attacker front-runs 1 of 3 streams, entire batch reverts.
    ///         1. Operator constructs 3 deposit streams for Alice
    ///         2. Attacker front-runs stream[2] with single depositByDelegation
    ///         3. Stream[2] consumed, operator's batch reverts entirely
    ///         4. Only 1 of 3 users served, operator gas wasted on full batch
    function test_POC_batchGriefingViaSingleFrontRun() public {
        uint256 aliceUSDCBefore_ = USDC.balanceOf(address(users.alice.deleGator));

        VedaAdapter.DepositParams[] memory streams_ = new VedaAdapter.DepositParams[](3);
        Delegation[] memory frontRunTarget_;

        // Build stream 0 (200 USDC, salt 100) — scoped to free stack
        {
            Delegation memory d_ = _createTransferDelegationWithSalt(
                address(users.bob.deleGator), address(vedaAdapter), address(USDC), type(uint256).max, 100
            );
            Delegation memory r_ =
                _createAdapterRedelegationWithSalt(EncoderLib._getDelegationHash(d_), address(USDC), 200e6, 100);
            Delegation[] memory c_ = new Delegation[](2);
            c_[0] = r_;
            c_[1] = d_;
            streams_[0] = VedaAdapter.DepositParams({ delegations: c_, minimumMint: 0 });
        }

        // Build stream 1 (300 USDC, salt 101)
        {
            Delegation memory d_ = _createTransferDelegationWithSalt(
                address(users.bob.deleGator), address(vedaAdapter), address(USDC), type(uint256).max, 101
            );
            Delegation memory r_ =
                _createAdapterRedelegationWithSalt(EncoderLib._getDelegationHash(d_), address(USDC), 300e6, 101);
            Delegation[] memory c_ = new Delegation[](2);
            c_[0] = r_;
            c_[1] = d_;
            streams_[1] = VedaAdapter.DepositParams({ delegations: c_, minimumMint: 0 });
        }

        // Build stream 2 (500 USDC, salt 102) — attacker will front-run this one
        {
            Delegation memory d_ = _createTransferDelegationWithSalt(
                address(users.bob.deleGator), address(vedaAdapter), address(USDC), type(uint256).max, 102
            );
            Delegation memory r_ =
                _createAdapterRedelegationWithSalt(EncoderLib._getDelegationHash(d_), address(USDC), 500e6, 102);
            Delegation[] memory c_ = new Delegation[](2);
            c_[0] = r_;
            c_[1] = d_;
            streams_[2] = VedaAdapter.DepositParams({ delegations: c_, minimumMint: 0 });
            frontRunTarget_ = c_;
        }

        // 2: Attacker front-runs with stream 2's delegation only
        vm.prank(makeAddr("Attacker"));
        vedaAdapter.depositByDelegation(frontRunTarget_, 0);

        assertGt(BORING_VAULT.balanceOf(address(users.alice.deleGator)), 0, "Alice got shares from front-run");

        // 3: Operator submits full 3-stream batch — reverts on consumed stream 2
        vm.prank(address(users.bob.deleGator));
        vm.expectRevert("ERC20TransferAmountEnforcer:allowance-exceeded");
        vedaAdapter.depositByDelegationBatch(streams_);

        // 4: Only stream 2 (500 USDC) executed. Streams 0+1 NOT served.
        assertEq(
            USDC.balanceOf(address(users.alice.deleGator)),
            aliceUSDCBefore_ - 500e6,
            "Only front-run stream executed. Batch streams 0 and 1 NOT served"
        );
    }
```

**Recommended Mitigation:** If public batching is expected to remain viable, the protocol should adopt one of these approaches:

1. **Use private orderflow for batch submission**
Submit batches through a private mempool so delegation streams are not exposed for mempool front-running before inclusion.

2. **Change batch semantics to tolerate per-stream failure**
Redesign batching to isolate failures per stream, for example by using external self-calls with `try/catch` and emitting per-stream failure events.

**Metamask:**
Acknowledged. We agree that, in a fully public mempool setting, the described behavior can create an economically griefable pattern for batch execution, since a single pre‑consumed delegation can cause an otherwise valid batch to revert. In practice, our operational model mitigates this in two ways: 1. We use a private mempool / private orderflow for submitting batch transactions, which substantially reduces the feasibility of mempool‑based front‑running and griefing of this kind. 2. Our backend batch orchestration logic detects failed delegations within a batch. If a delegation has already been consumed or is otherwise invalid, our system automatically adjusts the batch (e.g., by removing or correcting failing items) before resubmitting, thereby limiting the operational impact and cost of such failures. Given these measures, we consider the residual risk to be operational rather than a direct safety issue.

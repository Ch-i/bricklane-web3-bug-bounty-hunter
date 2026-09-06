---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-3-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: Excess ETH not refunded in non-adapter vault redemption
vuln_class: []
---

# Excess ETH not refunded in non-adapter vault redemption

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** In `SablierBob::redeem` (`SablierBob.sol:346-366`), for non-adapter vaults, the entire `msg.value` is forwarded to the comptroller without refunding any excess:

```solidity
uint256 minFeeWei = comptroller.calculateMinFeeWei({ protocol: ISablierComptroller.Protocol.Bob });

if (msg.value < minFeeWei) {
    revert Errors.SablierBob_InsufficientFeePayment(msg.value, minFeeWei);
}

if (msg.value > 0) {
    (bool success,) = address(comptroller).call{ value: msg.value }("");
    if (!success) {
        revert Errors.SablierBob_NativeFeeTransferFailed();
    }
}
```

There is no refund of `msg.value - minFeeWei` to the caller.

**Impact:** If a user sends more ETH than the minimum fee (e.g., sends 1 ETH when `minFeeWei` is 0.001 ETH), the entire 1 ETH goes to the comptroller and the excess 0.999 ETH is permanently lost to the user. This is especially likely if:
- Users overestimate the required fee to avoid reverts
- `minFeeWei` changes between transaction submission and mining (user sends extra as buffer)
- Frontend miscalculates the fee amount

**Proof of Concept:** Add the following test to `tests/bob/integration/concrete/redeem/redeemPoC.t.sol`:

```solidity
/// The ENTIRE msg.value is forwarded to the comptroller, even if it far exceeds
/// the minimum required fee. Users who overpay lose the excess permanently
function test_ExcessETHNotRefunded() external {
    // Set a non-zero minimum fee
    setMsgSender(admin);
    comptroller.setMinFeeUSD(ISablierComptroller.Protocol.Bob, 1e8); // $1

    // Create vault, deposit, expire
    setMsgSender(users.depositor);
    uint256 vaultId = createDefaultVault();
    bob.enter(vaultId, DEPOSIT_AMOUNT);
    vm.warp(EXPIRY + 1);

    // Get minFee and send 10x that amount
    uint256 minFee =
        comptroller.calculateMinFeeWeiFor({ protocol: ISablierComptroller.Protocol.Bob, user: users.depositor });
    assertGt(minFee, 0, "minFee should be > 0");
    uint256 overpayment = minFee * 10;

    uint256 comptrollerBefore = address(comptroller).balance;

    bob.redeem{ value: overpayment }(vaultId);

    // Entire overpayment went to comptroller - no refund to user
    assertEq(
        address(comptroller).balance - comptrollerBefore,
        overpayment,
        "CONFIRMED: full overpayment sent, no refund"
    );
}
```

Run with: `forge test --match-test test_ExcessETHNotRefunded -vvv`

**Recommended Mitigation:** Only forward the required fee and refund the excess (or alternatively, use `require(msg.value == minFeeWei)` to enforce exact payment):
```solidity
if (msg.value > 0) {
    uint256 feeToSend = minFeeWei;
    (bool success,) = address(comptroller).call{ value: feeToSend }("");
    if (!success) {
        revert Errors.SablierBob_NativeFeeTransferFailed();
    }
    // Refund excess
    uint256 excess = msg.value - feeToSend;
    if (excess > 0) {
        (bool refundSuccess,) = msg.sender.call{ value: excess }("");
        if (!refundSuccess) {
            revert Errors.SablierBob_NativeRefundFailed();
        }
    }
}
```

**Sablier:** Acknowledged; this is by design and a business decision.

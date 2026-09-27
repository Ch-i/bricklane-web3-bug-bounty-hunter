---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2-0-0-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-09-07T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2-0
title: '`DSToken::setOverCapDelay, setMintCap` never validate `overCapDelay` and documented
  48hr timelock delay useless vs 5hr overcap delay'
vuln_class: []
---

# `DSToken::setOverCapDelay, setMintCap` never validate `overCapDelay` and documented 48hr timelock delay useless vs 5hr overcap delay

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md)_

---

**Description:** `DSToken::setMintCap` validates its own parameter pair but does not require `overCapDelay` to be set and `setOverCapDelay` accepts any `uint256` with no validation at all. Enabling the allowance therefore produces a token where it is enforced on the normal path and simultaneously bypassable in one transaction, with no event distinguishing the two. The deployment runbook has no mint-control configuration step, so nothing directs an operator to set the delay first.

Above zero a second problem remains. `DSToken::cancelOverCapMint` is `onlyMaster`, and after handover master authority is the master timelock, so cancelling is itself a queued operation: schedule, wait `minDelay`, execute. A cancel beats the mint only where `overCapDelay` exceeds the master delay plus detection and human response time. Nothing links the two values: the master delay is a constructor argument of the controller, `overCapDelay` is token storage set by an unrelated later transaction, and a subsequent `updateDelay` raising the master delay silently invalidates a previously safe pairing. The worked example in the design notes uses 5 hour overcap delay against 48 hour timelock delay which renders the timelock cancel ineffective:

* 5 hours overcap delay: docs/bc-2132-mint-throttling-flows.md, Flow 7 (the happy-path walkthrough), at lines 160-167:
>
> readyAt:   now + overCapDelay,    // e.g. now + 5h
> expiresAt: now + overCapDelay + overCapGracePeriod,  // e.g. now + 29h
> ...
> --- wait overCapDelay (5 hours) ---
>

It's not a one-off. The same 5h carries through Flow 8 (line 187), Flow 9 (lines 202-209) and Flow 10 (line 221), so it's the document's working assumption for `overCapDelay` throughout, not a stray number in one example.

* 48 hours timelock delay in three places, consistent:
> - tasks/deploy-timelocks.ts:19 — .addOptionalParam('masterDelay', ..., 172800, types.int)
> - docs/runbooks/governance-timelocks.md:9 and :26 — the suggested minDelay table entry, and the literal --master-delay 172800 in the deploy command
> - docs/timelocks.md:90 — FR-1's implementation reference, "delays 172800 / 86400 / 86400 seconds as deployment defaults"
>

**Impact:** In the post-upgrade default state the exceptional path is an unconditional allowance bypass for any `ROLE_ISSUER` holder, bounded only by the operator remembering to set a delay that has no default and no prompt. Once a non-zero delay is set but chosen below the master delay (per the design docs 5hr overcap delay & 48hr timelock delay), scheduled mints become observable through `OverCapMintScheduled` yet unstoppable, because the cancel matures after the mint executes.

**Recommended Mitigation:** The durable fix is to stop requiring `overCapDelay` to outrun the master delay, rather than to police a relationship between two values set in different places at different times.

Cancellation is fail-safe: a wrongful cancel delays a re-schedulable subscription, while a missed cancel is unbounded issuance. The deployment already creates principals able to act inside the delay, since `TimelockController` grants `CANCELLER_ROLE` to every proposer and the runbook requires cancellers to be direct wallets precisely so cancellation can outrun a delay. Change `DSToken::cancelOverCapMint` to allow holders of `CANCELLER_ROLE` in the timelock to cancel pending overcap mints:

```solidity
function cancelOverCapMint(bytes32 _operationId) external override {
    require(_canCancelOverCapMint(msg.sender), "Insufficient trust level");
    // unchanged below
}

function _canCancelOverCapMint(address _who) internal view returns (bool) {
    if (owner() == _who) return true;
    if (getTrustService().getRole(_who) == ROLE_MASTER) return true;

    address masterTimelock = getDSService(MASTER_TIMELOCK);
    if (masterTimelock != address(0)) {
        try IAccessControl(masterTimelock).hasRole(CANCELLER_ROLE, _who) returns (bool ok) {
            return ok;
        } catch {}
    }
    return false;
}
```

`overCapDelay` then only has to exceed human response time, so it can be chosen on operational grounds without reference to the master delay.

Independently, make the unsafe intermediate state unreachable in both directions:

```solidity
// setMintCap
require(_mintCapAmount == 0 || overCapDelay > 0, "Over-cap delay must be set when cap is active");

// setOverCapDelay
require(_overCapDelay > 0 || mintCapAmount == 0, "Over-cap delay must be > 0 while cap is active");
```

**Securitize:** Fixed in commit [9595027](https://github.com/securitize-io/dstoken/commit/9595027e0113dd8525c762a99352809f79628845) by:
* adding recommended `require` statements in `setMintCap, setOverCapDelay`
* changing `cancelOverCapMint` to allow cancellation by `onlyIssuerOrTransferAgentOrAbove` instead of `onlyMaster`

**Cyfrin:** Verified. One consequence of the chosen fix is that any issuer can DoS other issuers' scheduled mints by cancelling them, however the timelock can revoke the role of malicious issuers so this is temporary and can be resolved.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-10-cyfrin-benqi-governance-v2-0-1-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-11-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-10-cyfrin-benqi-governance-v2-0
title: Unsafe transfer of non-standard ERC-20 tokens
vuln_class: []
---

# Unsafe transfer of non-standard ERC-20 tokens

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-10-cyfrin-benqi-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md)_

---

**Description:** The `DistributionManager` uses the standard ERC-20 `transfer()` function instead of a safe transfer equivalent when distributing reward tokens to controllers. While the reward token (QI) is a known, trusted contract that conforms to the ERC-20 specification, direct use of `transfer()` can lead to silent failures if this is not the case and the token does not correctly conform to the standard.

```solidity
// DistributionManager.sol - Lines 416-424
actions[actionCount++] = Action({
    to: address(rewardToken),
    value: 0,
    data: abi.encodeWithSelector(
        IERC20.transfer.selector, // @audit - uses transfer, not safeTransfer
        controller,
        amountWithBuffer
    )
});
```

The standard `IERC20::transfer` may:
* Return false on failure without reverting (e.g. USDT).
* Not return any value at all (e.g. BNB)

In both cases, the transaction would continue executing, the epoch would be marked as distributed, but the controller would not receive the tokens. This creates an inconsistent state where distribution appears successful but tokens were never transferred.

**Recommended Mitigation:** Consider using a checked safe transfer equivalent instead of direct ERC-20 transfer.

**BENQI:** Acknowledged.

**Cyfrin:** Acknowledged.

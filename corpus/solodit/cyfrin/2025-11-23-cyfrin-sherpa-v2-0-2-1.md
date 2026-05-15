---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-23-cyfrin-sherpa-v2-0-2-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-11-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-23-cyfrin-sherpa-v2-0
title: '`SherpaUSD::consumeTotalStakedApproval` and `SherpaUSD::consumeAccountingApproval`
  callable by anyone'
vuln_class: []
---

# `SherpaUSD::consumeTotalStakedApproval` and `SherpaUSD::consumeAccountingApproval` callable by anyone

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-23-cyfrin-sherpa-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md)_

---

**Description:** In the rebalancing/settlement flow for cross-chain accounting, [`SherpaUSD::consumeTotalStakedApproval`](48a767f7ed2265404c59592c098b7/contracts/SherpaUSD.sol#L282-L291) and [`SherpaUSD::consumeAccountingApproval`](https://github.com/hedgemonyxyz/sherpa-vault-smartcontracts/blob/50eb8ad6ee048a767f7ed2265404c59592c098b7/contracts/SherpaUSD.sol#L293-L302) serve as the “consume/clear” step for one-time approvals set by `SherpaUSD::ownerMint`/`SherpaUSD::ownerBurn`. They are invoked around `SherpaVault::adjustTotalStaked` and `SherpaVault::adjustAccountingSupply` to prevent reuse of an approval after the corresponding adjustment is applied.

Both functions are externally callable and accept a `vault` parameter, but state changes are gated by `if (msg.sender != vault) revert OnlyVaultCanConsume();` and approvals are keyed by the caller address:
```solidity
function consumeTotalStakedApproval(address vault) external {
    // @audit-issue anyone can call by passing their own address as `vault`
    if (msg.sender != vault) revert OnlyVaultCanConsume();
    approvedTotalStakedAdjustment[vault] = 0;
    emit TotalStakedApprovalConsumed(vault);
}
```
Consequently, any address may call the functions, yet the call can only clear its own approval entry, not a vault’s. Behavior is correct and non-exploitable in this design; however, the open callable surface combined with an explicit `vault` parameter can be confusing to integrators and reviewers.

Consider removing the `vault` parameter and only allow the actual vault to call by adding the `onlyKeeper` modifier. This would follow the principle of least privilege and limit the attack surfaces available.

**Sherpa:** Fixed in commit [`c33eb52`](https://github.com/hedgemonyxyz/sherpa-vault-smartcontracts/commit/c33eb5212430b6c4115be9f87950e47540f20522)

**Cyfrin:** Verified. Both functions now have the `vault` parameter removed and the `onlyKeeper` modifier.

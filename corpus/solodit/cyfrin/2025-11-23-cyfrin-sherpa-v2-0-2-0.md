---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-23-cyfrin-sherpa-v2-0-2-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-11-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-23-cyfrin-sherpa-v2-0
title: '`SherpaVault::_rollInternal` price calculation comment and math inconsistent'
vuln_class: []
---

# `SherpaVault::_rollInternal` price calculation comment and math inconsistent

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-23-cyfrin-sherpa-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md)_

---

**Description:** When calculating a new price a script queries all vaults on all chains then passes that to `SherpaVault:: rollToNextRound`. This in turn calls [`SherpaVault::_rollInternal`](https://github.com/hedgemonyxyz/sherpa-vault-smartcontracts/blob/50eb8ad6ee048a767f7ed2265404c59592c098b7/contracts/SherpaVault.sol#L518-L529) where the new price is calculated:
```solidity
// Calculate global price using script-provided totals
// globalBalance must include pending deposits for correct price calculation
uint256 globalBalance = isYieldPositive
    ? globalTotalStaked + globalTotalPending + yield
    : globalTotalStaked + globalTotalPending - yield;

uint256 newPricePerShare = ShareMath.pricePerShare(
    globalShareSupply,
    globalBalance,
    globalTotalPending,
    _vaultParams.decimals
);
```
The code comments state that `globalBalance must include pending deposits` yet `globalBalance` is passed to [`ShareMath:pricePerShare`](https://github.com/hedgemonyxyz/sherpa-vault-smartcontracts/blob/50eb8ad6ee048a767f7ed2265404c59592c098b7/contracts/lib/ShareMath.sol#L66-L77), which immediately subtracts the `pending` amount: (`(totalBalance - pending) / totalSupply`):
```solidity
function pricePerShare(
    uint256 totalSupply,   // @audit-info globalShareSupply
    uint256 totalBalance,  // @audit-info globalBalance
    uint256 pendingAmount, // @audit-info globalTotalPending
    uint256 decimals
) internal pure returns (uint256) {
    uint256 singleShare = 10 ** decimals;
    return
        totalSupply > 0
            ? (singleShare * (totalBalance - pendingAmount)) / totalSupply
            : singleShare;
}
```
The comment in `_rollInternal` is inconsistent with the math applied as the actual price calculation doesn't include the `pendingAmount`.

Consider changing the comment or if the comment is correct, the math.


**Sherpa:** Fixed in commit [`9dbaf27`](https://github.com/hedgemonyxyz/sherpa-vault-smartcontracts/commit/9dbaf277ec7b7349af682aa5d9f6a6ae78151db9)

**Cyfrin:** Verified. Comment was incorrect and is not fixed.

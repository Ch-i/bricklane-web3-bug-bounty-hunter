---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-31-cyfrin-linea-tokens-v2-3-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-07-31T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-31-cyfrin-linea-tokens-v2.3.md
tags:
- firm:cyfrin
- report:2025-07-31-cyfrin-linea-tokens-v2-3
title: Mismatched total supply cap between L1 and L2 tokens
vuln_class: []
---

# Mismatched total supply cap between L1 and L2 tokens

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-31-cyfrin-linea-tokens-v2.3.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-31-cyfrin-linea-tokens-v2.3.md)_

---

**Description:** OpenZeppelin’s [`ERC20VotesUpgradeable`](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/release-v5.4/contracts/token/ERC20/extensions/ERC20VotesUpgradeable.sol#L45-L47) enforces:

```solidity
function _maxSupply() internal view virtual returns (uint256) {
    return type(uint208).max;
}
```
to keep vote‑checkpoint values within 208 bits. As a result, any L1 total supply above `2^208 − 1` would be valid on L1, as the standard ERC20 implementation uses `type(uint256).max`, but invalid on L2. However, since `type(uint208).max` is astronomically larger than any realistic token issuance, this is extremely unlikely in practice.

If strict symmetry is preferred, consider enforcing the same `uint208` cap on L1, via [`ERC20CappedUpgradeable`](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/release-v5.4/contracts/token/ERC20/extensions/ERC20CappedUpgradeable.sol) or a manual `require(totalSupply() + mintAmount <= type(uint208).max)` in `mint()`, so both chains’ supply limits are aligned.

**Linea:** Acknowledged.

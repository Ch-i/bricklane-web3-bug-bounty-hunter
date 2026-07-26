---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-23-cyfrin-sherpa-v2-0-1-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-11-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-23-cyfrin-sherpa-v2-0
title: Direct amount assignment in `SherpaUSD::ownerMint`/`ownerBurn` can break accounting
  for totalStaked and accountingSupply
vuln_class: []
---

# Direct amount assignment in `SherpaUSD::ownerMint`/`ownerBurn` can break accounting for totalStaked and accountingSupply

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-23-cyfrin-sherpa-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md)_

---

**Description:** Functions `SherpaUSD::ownerMint` and `ownerBurn` directly assign the amount parameter to mappings `approvedTotalStakedAdjustment` and `approvedAccountingAdjustment`. This will however not work correctly if more tokens are minted or burned to/from the vault before the approvals are consumed.

For example:
 - Operator mints 100 SherpaUSD to SherpaVault.
 - This tracks `approvedTotalStakedAdjustment` and `approvedAccountingAdjustment` as 100 SherpaUSD each
 - Operator performs another mint of 200 tokens before the previous approvals are consumed.
 - Now the issue is that approvedTotalStakedAdjustment and approvedAccountingAdjustment will be overwritten to store 200 SherpaUSD each instead of 300 SherpaUSD.
 - This is clearly incorrect and breaks accounting since old approvals were not consumed yet by the vault.

```solidity
function ownerMint(address to, uint256 amount) external onlyOperator {
    _mint(to, amount);

    // Approve vault to adjust by this amount
    approvedTotalStakedAdjustment[to] = amount;
    approvedAccountingAdjustment[to] = amount;

    emit PermissionedMint(to, amount);
    emit RebalanceApprovalSet(to, amount, amount);
}

/**
 * @notice Operator-level burn for manual rebalancing across chains
 * @param from Address to burn from
 * @param amount Amount to burn
 * @dev Sets approval for vault to adjust totalStaked and accountingSupply
 */
function ownerBurn(address from, uint256 amount) external onlyOperator {
    _burn(from, amount);

    // Approve vault to adjust by this amount
    approvedTotalStakedAdjustment[from] = amount;
    approvedAccountingAdjustment[from] = amount;

    emit PermissionedBurn(from, amount);
    emit RebalanceApprovalSet(from, amount, amount);
}
```

**Recommended Mitigation:** Consider replacing direct amount assignments with the += and -= operators in ownerMint and ownerBurn respectively.

**Sherpa:** Fixed in commit [`1cd0018`](https://github.com/hedgemonyxyz/sherpa-vault-smartcontracts/commit/1cd00183932d086b0fd07d6c34cd3f5aacb2b359)

**Cyfrin:** Verified. Checks to enforce that the approvals have been consumed are added. This prevents any accounting corruption.

\clearpage

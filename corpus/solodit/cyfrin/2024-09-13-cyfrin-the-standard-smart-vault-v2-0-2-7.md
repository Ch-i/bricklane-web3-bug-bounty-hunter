---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-09-13-cyfrin-the-standard-smart-vault-v2-0-2-7
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-09-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md
tags:
- firm:cyfrin
- report:2024-09-13-cyfrin-the-standard-smart-vault-v2-0
title: Collateral tokens with more than 18 decimals are not supported
vuln_class: []
---

# Collateral tokens with more than 18 decimals are not supported

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md)_

---

**Description:** Due to the existing decimals scaling logic within [`PriceCalculator::getTokenScaleDiff`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/PriceCalculator.sol#L15-L17), any collateral tokens with more than 18 decimals will not be supported and will result in DoS of Smart Vault functionality:

```solidity
function getTokenScaleDiff(bytes32 _symbol, address _tokenAddress) private view returns (uint256 scaleDiff) {
    return _symbol == NATIVE ? 0 : 18 - ERC20(_tokenAddress).decimals();
}
```

Similar scaling is present in [`SmartVaultV4::yieldVaultCollateral`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultV4.sol#L92-L93); however, this would require another `USDs` Hypervisor with a problematic underlying token to be added, which is unlikely.

**Impact:** Smart Vault collateral cannot be calculated if a token with more than 18 decimals is added to the list of accepted tokens, resulting in denial-of-service.


**Recommended Mitigation:** Consider scaling to a greater number of decimals if collateral tokens with more than 18 decimals will be added.

**The Standard DAO:** Fixed by commit [`cf871f7`](https://github.com/the-standard/smart-vault/commit/cf871f7950465904f3f8967e6504eacdd1cbc75c) – not suitable for hypervisor deposits, but should be ok for collateral.

**Cyfrin:** Verified, now supports collateral tokens with more than 18 decimals; however, division before multiplication for the `scale < 0` branch` could be problematic – it might be better to first scale all decimals to 36 and then divide back down to 18 in the return statement of `tokenToUSD`.

**The Standard DAO:** Fixed in commit [`2342302`](https://github.com/the-standard/smart-vault/commit/23423024550bca2dbe182e079403b28cc8d1f6e9).

**Cyfrin:** Verified, now scales decimals to 36 before rescaling back down to 18.

\clearpage

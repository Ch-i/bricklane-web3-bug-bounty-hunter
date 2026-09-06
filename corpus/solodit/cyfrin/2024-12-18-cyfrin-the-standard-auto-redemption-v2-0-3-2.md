---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-3-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-12-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-18-cyfrin-the-standard-auto-redemption-v2-0
title: Unused response parameter should be removed
vuln_class: []
---

# Unused response parameter should be removed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md)_

---

**Description:** The `_estimatedCollateralValueUSD` parameter decoded from the Chainlink Functions response and passed as an argument to `AutoRedemption::legacyAutoRedemption` is not used and can be removed:

```solidity
(uint256 _tokenID, address _token, uint256 _estimatedCollateralValueUSD) =
    abi.decode(response, (uint256, address, uint256));
...
legacyAutoRedemption(
    _smartVault, _token, _collateralToUSDCPath, _USDsTargetAmount, _estimatedCollateralValueUSD
);
```

**The Standard DAO:** Fixed by commit [59c4bd5](https://github.com/the-standard/smart-vault/commit/59c4bd57f1d15c8d8eeb3965368f21e78594186c).

**Cyfrin:** Verified. The parameter has been removed and the source/decoding/signatures have been updated accordingly.

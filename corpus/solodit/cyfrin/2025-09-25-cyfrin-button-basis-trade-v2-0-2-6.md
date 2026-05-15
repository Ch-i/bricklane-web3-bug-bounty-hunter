---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-25-cyfrin-button-basis-trade-v2-0-2-6
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-09-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-25-cyfrin-button-basis-trade-v2-0
title: Lack of check for 0 shares minted
vuln_class: []
---

# Lack of check for 0 shares minted

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-25-cyfrin-button-basis-trade-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md)_

---

**Description:** `previewDeposit(assets)` can legitimately return `0` shares for tiny deposits due to rounding and/or deposit fees. If the deposit path doesn’t guard against this, a user could transfer assets to the vault and receive 0 shares (an unintended “donation”).

Consider adding a check for 0 shares:
```solidity
function previewDeposit(uint256 assets) public view virtual override returns (uint256) {
    uint256 fee = _extractFeeFromTotal(assets, depositFeeBps);
    require(fee < assets, "Deposit fee exceeds assets");
    uint256 shares = super.previewDeposit(assets - fee);
    require(shares > 0, "0 shares");
    return shares;
}
```


**Button:** Fixed in commit [`9cde24c`](https://github.com/buttonxyz/button-protocol/commit/9cde24caa4b3f5f37a059bb2fde172cfa374d3a9)

**Cyfrin:** Verified. `previewDeposit` now checks that `> 0 shares` are minted.

\clearpage

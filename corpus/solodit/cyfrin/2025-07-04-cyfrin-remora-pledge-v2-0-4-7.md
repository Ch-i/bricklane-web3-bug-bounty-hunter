---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-4-7
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: In `RemoraToken::adminClaimPayout`, `adminTransferFrom` don't call `hasSignedDocs`
  when `checkTC == false`
vuln_class: []
---

# In `RemoraToken::adminClaimPayout`, `adminTransferFrom` don't call `hasSignedDocs` when `checkTC == false`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** In `RemoraToken::adminClaimPayout` don't call `hasSignedDocs` when `checkTC == false` to prevent doing unnecessary work:
```solidity
function adminClaimPayout(
    address investor,
    bool useStablecoin,
    bool useCustomFee,
    bool checkTC,
    uint256 feeValue
) external nonReentrant restricted {
    if(checkTC) {
        (bool res, ) = hasSignedDocs(investor);
        if (!res) revert TermsAndConditionsNotSigned(investor);
    }

    _claimPayout(investor, useStablecoin, useCustomFee, feeValue);
}
```

Apply similar fix to `adminTransferFrom`.

**Remora:** Fixed in commit [a5c03d4](https://github.com/remora-projects/remora-smart-contracts/commit/a5c03d4d22a783e3ab7966a7e573724648cad0a9).

**Cyfrin:** Verified.

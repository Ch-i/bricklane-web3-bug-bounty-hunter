---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-13-cyfrin-safe-harbor-v2-0-2-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-01-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-13-cyfrin-safe-harbor-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-13-cyfrin-safe-harbor-v2-0
title: Missing contact details validation
vuln_class: []
---

# Missing contact details validation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-13-cyfrin-safe-harbor-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-13-cyfrin-safe-harbor-v2.0.md)_

---

**Description:** `Agreement::_setDetails` copies contact details without any validation. The `Contact` struct fields can contain empty strings:

Neither the constructor nor `setContactDetails` validates that contact fields are non-empty:

```solidity
function _setDetails(AgreementDetails memory _details) internal {
     // code...
     delete contactDetails;
     for (uint256 i = 0; i < _details.contactDetails.length; ++i) {
         contactDetails.push(_details.contactDetails[i]); //@audit no check for empty name or contact
      }
}

function setContactDetails(Contact[] memory _contactDetails) external onlyOwner {
    emit ContactDetailsSet(_contactDetails);
    delete contactDetails;
    for (uint256 i = 0; i < _contactDetails.length; i++) {
        contactDetails.push(_contactDetails[i]); //@audit no check for empty name or contact
    }
}
```

**Impact:** Whitehats rely on contact details for prior notification before rescue operations. Empty or invalid contact information could prevent whitehats from reaching out to protocol teams effectively.

**Recommended Mitigation:** Consider adding validation for contact details. Alternatively, document that empty contacts are allowed.

**SafeHarbor:**
Fixed in [0f492fc](https://github.com/PatrickAlphaC/safe-harbor/commit/0f492fc78088a5dca4adc7201b669f92fab17b7f).

**Cyfrin:** Verified.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-03-cyfrin-linea-burn-v2-2-1-8
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-11-03T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-03-cyfrin-linea-burn-v2.2.md
tags:
- firm:cyfrin
- report:2025-11-03-cyfrin-linea-burn-v2-2
title: Function updateInvoiceArrears() updates `lastInvoiceDate` even when `invoiceArrears`
  remains unchanged
vuln_class: []
---

# Function updateInvoiceArrears() updates `lastInvoiceDate` even when `invoiceArrears` remains unchanged

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-03-cyfrin-linea-burn-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-03-cyfrin-linea-burn-v2.2.md)_

---

**Description:** Function updateInvoiceArrears() allows the DEFAULT_ADMIN_ROLE to update the `invoiceArrears` variable as well as `lastInvoiceDate` accordingly. However, even if the `invoiceArrears` variable remains unchanged, `lastInvoiceDate` can still be updated to a different timestamp.

```solidity
function updateInvoiceArrears(
    uint256 _newInvoiceArrears,
    uint256 _lastInvoiceDate
  ) external onlyRole(DEFAULT_ADMIN_ROLE) {
    require(_lastInvoiceDate >= lastInvoiceDate, InvoiceDateTooOld());

    invoiceArrears = _newInvoiceArrears;
    lastInvoiceDate = _lastInvoiceDate;

    emit InvoiceArrearsUpdated(_newInvoiceArrears, _lastInvoiceDate);
  }
```


**Impact:** Variable `lastInvoiceDate` is updated even when `invoiceArrears` is not updated.

**Proof of Concept:** **Recommended Mitigation:**
Consider disallowing this behaviour by implementing a check to ensure `_newInvoiceArrears` is not equal to `invoiceArrears`. Alternatively, if such behaviour is intended, consider renaming the function to `updateInvoiceArrearsAndLastInvoiceDate`.

**Linea:** Acknowledged, this accounts for various flexible situations and ways we can correct slow infrastructure billing updates.

**Cyfrin:** Acknowledged.

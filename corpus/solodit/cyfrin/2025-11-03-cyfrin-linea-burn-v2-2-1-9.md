---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-03-cyfrin-linea-burn-v2-2-1-9
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-11-03T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-03-cyfrin-linea-burn-v2.2.md
tags:
- firm:cyfrin
- report:2025-11-03-cyfrin-linea-burn-v2-2
title: Function updateInvoiceArrears() does not emit old values
vuln_class: []
---

# Function updateInvoiceArrears() does not emit old values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-03-cyfrin-linea-burn-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-03-cyfrin-linea-burn-v2.2.md)_

---

**Description:** Function updateInvoiceArrears() should consider emitting previous `invoiceArrears` and `lastInvoiceDate` values to maintain consistency with other setter functions updateL1LineaTokenBurner, updateDex and updateInvoicePaymentReceiver that emit both old and new values in their events.

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

**Impact:** **Proof of Concept:**

**Recommended Mitigation:** Emit old `invoiceArrears` and `lastInvoiceDate` values in event `InvoiceArrearsUpdated`.

**Linea:** Fixed in commit [6c65701](https://github.com/Consensys/linea-monorepo/pull/1620/commits/6c6570123e25d5e9ecb98df5b663f5030281f3bb)

**Cyfrin:** Verified.

\clearpage

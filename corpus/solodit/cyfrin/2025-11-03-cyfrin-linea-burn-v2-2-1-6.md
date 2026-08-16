---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-03-cyfrin-linea-burn-v2-2-1-6
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-11-03T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-03-cyfrin-linea-burn-v2.2.md
tags:
- firm:cyfrin
- report:2025-11-03-cyfrin-linea-burn-v2-2
title: Condition `_invoiceAmount != 0` in submitInvoice() can prevent clearing existing
  debt
vuln_class: []
---

# Condition `_invoiceAmount != 0` in submitInvoice() can prevent clearing existing debt

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-03-cyfrin-linea-burn-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-03-cyfrin-linea-burn-v2.2.md)_

---

**Description:** Function submitInvoice() implements the following check below:

```solidity
require(_invoiceAmount != 0, ZeroInvoiceAmount());
```

However, if the INVOICE_SUBMITTER role wants to only clear `invoiceArrears` if sufficient ETH balance becomes available, it will not be able to do so. For example:

 - Assume at T1, `invoiceArrears` = 1e18 since there is not enough native token balance in the contract.
 - At T2, the contract receives 1e18 native token balance, which can be used to clear the existing debt stored in `invoiceArrears`.
 - However, `invoiceArrears` cannot be cleared by passing in `_invoiceAmount` as 0 due to the check in submitInvoice().

**Impact:** Although the INVOICE_SUBMITTER can wait until the next invoice submission, this delays payment of existing debt that could've been paid out sooner.

**Proof of Concept:** **Recommended Mitigation:**
Consider ackowledging this behaviour or implementing either one of the following fixes:
1. Remove the `_invoiceAmount != 0` condition.
2. Implement a separate function that allows clearing invoiceArrears.

**Linea:** Fixed in [PR 1637](https://github.com/Consensys/linea-monorepo/pull/1637/files).

**Cyfrin:** Verified.

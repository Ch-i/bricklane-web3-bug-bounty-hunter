---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-accountable-v2-0-4-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-accountable-v2-0
title: Consider enforcing a minimum deposit amount
vuln_class: []
---

# Consider enforcing a minimum deposit amount

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-accountable-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md)_

---

The vault/strategy accepts arbitrarily small deposits (down to 1 wei). While functionally correct, dust deposits are effectively useless for legitimate users (since the gas to call `deposit` often exceeds the value deposited) and can be abused by adversaries to abuse rounding edge cases.

To remove a possible attack vector for black hats, consider enforcing a `minimumDepositAmount`.

**Accountable:** Fixed in [`b9edb2b`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/b9edb2bf071db803fbd16460411688207aedc85d)

**Cyfrin:** Verified.

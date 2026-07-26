---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-30-cyfrin-accountable-pr75-v2-0-2-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-06-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-30-cyfrin-accountable-pr75-v2-0
title: '`DepositGateway::_refundable` carries an inverted minDeposit comment that
  misstates the setter-regression direction'
vuln_class: []
---

# `DepositGateway::_refundable` carries an inverted minDeposit comment that misstates the setter-regression direction

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-30-cyfrin-accountable-pr75-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md)_

---

**Description:** In `DepositGateway::_refundable`, the final branch is `if (strategy_.loan().minDeposit > assets) return true;`, preceded by the comment "If minDeposit was lowered after the request was made, it is refundable". The comment describes the wrong direction: `loan().minDeposit > assets` is true precisely when `minDeposit` has been *raised* above the amount the user already escrowed, which is the case that strands the request (a settle would now fail the strategy's minimum-deposit check, so the request must be refundable). The code is correct; the comment inverts the condition it documents. The hazard is drift: a future editor "fixing" the code to match the comment - changing the test to `minDeposit < assets` - would make legitimate requests that sit below the *current* minDeposit refundable and would stop refunding the raised-minimum requests that actually need it, breaking settlement for the exact population the branch exists to protect.

**Recommended Mitigation:** Correct the comment to match the code, e.g. "If minDeposit was raised above the escrowed amount after the request was made, the request can no longer be settled and is refundable". Leave the condition `strategy_.loan().minDeposit > assets` unchanged.

**Accountable:** Fixed in commit [`aea937c`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/aea937ccb0d39600236526c1dbcfe78fadbb3865)

**Cyfrin:** Verified.

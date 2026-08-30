---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-accountable-v2-0-2-8
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-accountable-v2-0
title: Withdrawal queue `RequestPrice` can be front run in case of defaults
vuln_class: []
---

# Withdrawal queue `RequestPrice` can be front run in case of defaults

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-accountable-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md)_

---

**Description:** When `processingMode == ProcessingMode.RequestPrice` in `AccountableWithdrawalQueue`, a redeem request’s value is fixed at the request-time share price. The request is later processed potentially at a very different price.

**Impact:** * Normal operation: Requesters are typically disadvantaged because price usually rises as interest accrues. Locking at request time forfeits subsequent gains.
* Defaults: Requesters can front-run defaults by submitting withdrawals just before delinquency/default and keep the pre-default higher price, draining liquidity and pushing losses onto remaining LPs. This worsens loss socialization precisely when fairness matters most.

**Recommended Mitigation:** Consider removing `ProcessingMode.RequestPrice` (and `AccountableWithdrawalQueue .processingMode` all together) so redemption value is always determined at processing time. Alternatively implement a safeguard for large price movements that will invalidate the redeem request.

**Accontable:**
Fixed in commit [`4e5eef5`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/4e5eef57464d548ec09048eae27b6fcc1489a5c3)

**Cyfrin:** Verified. `processingMode` removed and current price used throughout.

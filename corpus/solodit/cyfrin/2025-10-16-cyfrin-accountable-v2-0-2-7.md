---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-accountable-v2-0-2-7
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
title: Borrower in OpenTerm loan can stay delinquent effectively forever
vuln_class: []
---

# Borrower in OpenTerm loan can stay delinquent effectively forever

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-accountable-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md)_

---

**Description:** Delinquency is flagged when vault reserves fall below `_calculateRequiredLiquidity()`, setting `delinquencyStartTime`. Late penalties only accrue after the grace period elapses. If the borrower briefly restores liquidity (e.g., `supply()`/`repay()`) before grace expiry, delinquency is cleared and `delinquencyStartTime` resets to 0. The borrower can immediately `borrow()` again to drop reserves to the threshold and the next block, when interest has accrued again, start a fresh grace window. This “pulse” can be executed back-to-back, even within one block, allowing the borrower to remain effectively delinquent indefinitely without ever incurring penalties.

**Impact:** Borrowers can avoid late penalties while keeping lenders under-reserved, degrading lender protections.

**Recommended Mitigation:** Consider removing the grace period entirely so penalties accrue as soon as the loan becomes delinquent. This would reduce complexity and be in line with how a lot of other lending protocols work.

Alternatively consider redesigning the grace period to be cumulative, i.e. A year loan has a cumulative 1 week grace period which the borrower can draw from.

**Accountable:** We will acknowledge this. We don't have an actionable path on how loans are managed when it comes to penalties grace periods or even whether penalties are enabled or not. Having a considerable grace period is by design and as a fallback a manager can always initiate a default. In most use-cases borrow/repay actions won't be very often and given these entities deploy funds to other venues, also off-chain, doing such actions can come with a reputational cost.

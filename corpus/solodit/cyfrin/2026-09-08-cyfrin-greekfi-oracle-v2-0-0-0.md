---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-08-cyfrin-greekfi-oracle-v2-0-0-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-09-08T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-oracle-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-08-cyfrin-greekfi-oracle-v2-0
title: Post-deadline Receipt underpricing can cause premature liquidations
vuln_class: []
---

# Post-deadline Receipt underpricing can cause premature liquidations

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-08-cyfrin-greekfi-oracle-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-oracle-v2.0.md)_

---

**Description:** `OracleReceipt::price()` always values a Receipt as `1 - optionPrice`. After `exerciseDeadline`, it sets time to zero but continues valuing the expired exercise right at its current intrinsic value.

That is wrong for an unexercised Receipt. Assignment is closed, and when `consBacked == 0`, each Receipt is a fixed 1:1 collateral claim regardless of later spot movements.

A borrower can create this state by retaining the Options and supplying only the Receipts to Morpho. After the deadline, a spot movement can reduce the reported Receipt price even though the Receipts remain fully collateral-backed.

Morpho can then liquidate an adequately backed position using the incorrect price. An external liquidator can redeem the seized Receipts at par, transferring value from the borrower. Lenders are only exposed if the price gaps past the solvent liquidation range or liquidators fail to act.

**Impact:** The incorrect price can cause premature liquidation and loss for the borrower. With gradual price movement and active liquidators, the position becomes liquidatable while its collateral can still repay the debt in full. Lender loss requires a sufficiently large price gap or unavailable liquidators.

**Recommended Mitigation:** Return par after `exerciseDeadline` when `consBacked == 0`, without consulting the live spot price.

**GreekFi:** Fixed in [PR38](https://github.com/greekfi/contracts/pull/38).

**Cyfrin:** Verified. The oracle now returns par after the exercise deadline when `consBacked == 0`, so fully unexercised Receipts no longer follow the live spot price. Partially assigned series retain the documented conservative settlement mark as residual liquidation risk.

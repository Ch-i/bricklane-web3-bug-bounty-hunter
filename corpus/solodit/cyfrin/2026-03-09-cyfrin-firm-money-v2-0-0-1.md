---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-09-cyfrin-firm-money-v2-0-0-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-03-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-09-cyfrin-firm-money-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-09-cyfrin-firm-money-v2-0
title: Debt-limit enforcement is inconsistent with the stated requirement “being at
  or over the limit means debt can only be repaid or redeemed"
vuln_class: []
---

# Debt-limit enforcement is inconsistent with the stated requirement “being at or over the limit means debt can only be repaid or redeemed"

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-09-cyfrin-firm-money-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-09-cyfrin-firm-money-v2.0.md)_

---

**Description:** Debt-limit enforcement is inconsistent with the stated requirement “being at or over the limit means debt can only be repaid or redeemed.”

`BorrowerOperations` enforces debt limit in:
1. `openTrove` BorrowerOperations.sol:364
2. `adjustTrove` only when `debtIncrease > 0` BorrowerOperations.sol:665

However, debt can still increase through upfront-fee paths where `debtIncrease == 0`:
1. `_applyUpfrontFee` adds fee debt BorrowerOperations.sol:1181
2. Called from `adjustTroveInterestRate` BorrowerOperations.sol:543
3. Called from `setInterestBatchManager` BorrowerOperations.sol:1013
4. Called from `removeFromBatch` BorrowerOperations.sol:1129
5. Similar fee path in `setBatchManagerAnnualInterestRate` BorrowerOperations.sol:948

**Impact:** When branch debt is at/above `debtLimit`, users can still increase debt through fee-incurring adjustment operations, violating the intended branch cap behavior. This weakens governance risk controls and allows debt drift above limit via non-borrow operations.

**Proof of Concept:**
1. Set a branch debt limit close to current debt (or equal to current debt).
2. Use an existing active trove.
3. Trigger a premature interest-rate adjustment (within cooldown) via `adjustTroveInterestRate`.
4. `_applyUpfrontFee` computes a positive `upfrontFee` and adds it to trove debt.
5. No `_requireDebtLimitNotExceeded` check is executed on this path, so transaction succeeds even though branch debt increases above the limit.

Same pattern applies to `setInterestBatchManager`, `removeFromBatch`, and `setBatchManagerAnnualInterestRate`.

**Recommended Mitigation:** Enforce debt limit on **all positive net debt deltas**, not only explicit `debtIncrease`.

Practical fix:
1. Introduce a helper that checks projected branch debt with `delta = debtIncrease + upfrontFee - debtDecrease`.
2. Call it in every path that can add debt (including `_applyUpfrontFee` callers and batch fee-adjustment flows).
3. If behavior is intentionally “borrow-cap only,” update docs/specs to state that explicitly and remove “only repaid or redeemed” wording.

**Firm Money:**
Acknowledged. This is intended behavior, and an understood limitation listed in the hackmd. You dont want to stop interest from accruing, that creates more danger that could lead to bad debt.

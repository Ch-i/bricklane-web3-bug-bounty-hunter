---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-22-cyfrin-remora-dynamic-tokens-v2-1-2-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-10-22T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-22-cyfrin-remora-dynamic-tokens-v2-1
title: Allowance check in `FiveFiftyRule::canTransfer` is inverted
vuln_class: []
---

# Allowance check in `FiveFiftyRule::canTransfer` is inverted

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md)_

---

**Description:** The following snippet from `FiveFiftyRule::canTransfer` has inverted logic.

```solidity
            if (iTo.isEntity) { // if entity
@>              if (entityData[to].allowance <= amount) {
                    entityData[to].allowance -= SafeCast.toUint64(amount);

                    iTo.lastBalance += SafeCast.toUint64(amount);
                    emit FiveFiftyApproved(from, to, amount);
                    return true;
                } else revert ();
            }
```

This is also present in `FiveFiftyRule::checkCanTransfer`.

**Impact:** No transfers to entities are possible except in the rare cases that `allowance == amount`
In the other two cases the function will revert, but for different reasons.
- If `allowance  > amount` then function will revert due to the else-branch
- If `allowance < amount` then the function will revert due to underflow

**Recommended Mitigation:**
```diff
            if (iTo.isEntity) { // if entity
-               if (entityData[to].allowance <= amount) {
+               if (entityData[to].allowance >= amount) {
                    entityData[to].allowance -= SafeCast.toUint64(amount);
```

```diff
        if (iData.isEntity)
-           return entityData[to].allowance <= amount;
+           return entityData[to].allowance >= amount;
```

**Remora:** Fixed at commit [a69e893](https://github.com/remora-projects/remora-dynamic-tokens/commit/a69e89357e5180150894b8d8b24f273bdf45893c)

**Cyfrin:** Verified. Comparison operator has been inverted to use the correct operator.

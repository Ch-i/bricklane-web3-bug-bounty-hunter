---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-29-cyfrin-securitize-full-investor-locks-v2-0-1-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-05-29T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-29-cyfrin-securitize-full-investor-locks-v2-0
title: '`RegistryService::setAttribute` skips compliance counter reconciliation on
  ACCREDITED/QUALIFIED flips'
vuln_class: []
---

# `RegistryService::setAttribute` skips compliance counter reconciliation on ACCREDITED/QUALIFIED flips

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md)_

---

**Description:** `ComplianceServiceRegulated::adjustInvestorsCountsByCountry` (lines 688-735) maintains `accreditedInvestorsCount`, `usAccreditedInvestorsCount`, and `euRetailInvestorsCount[country]` by reading the CURRENT value of `isAccreditedInvestor(_id)` / `isQualifiedInvestor(_id)` at every increment/decrement.

`RegistryService::setAttribute` (lines 133-149) and `updateInvestor` (lines 60-93, which forwards into `setAttribute`) write the attribute mapping directly without notifying the compliance service:

```solidity
function setAttribute(string calldata _id, uint8 _attributeId, uint256 _value, ...) ... {
    attributes[_id][_attributeId].value = _value;
    // No call into compliance to reconcile counters.
}
```

If `setAttribute` flips an investor's ACCREDITED or QUALIFIED attribute while the investor has a non-zero balance, the next counter-touching event (full out-transfer, burn, seize) decrements a different counter than the one that was incremented at issuance.

**Files:**

`RegistryService::setAttribute, updateInvestor`, `ComplianceServiceRegulated::adjustInvestorsCountsByCountry`

**Impact:** If `setAttribute` flips ACCREDITED or QUALIFIED while the investor has a non-zero balance, the compliance counters drift: a non-accredited-to-accredited flip blocks the investor's next full out-transfer with an underflow revert on `accreditedInvestorsCount--` (locking the position; `recordBurn` and `recordSeize` are blocked identically), while an accredited-to-rejected flip permanently inflates `accreditedInvestorsCount` and causes subsequent non-accredited admissions to spuriously hit the `MAX_INVESTORS_IN_CATEGORY` cap because `getTotalInvestorsCount() - getAccreditedInvestorsCount()` under-reports the non-accredited headroom. The QUALIFIED mirror produces the same shape on `euRetailInvestorsCount[country]`. The protocol team can avoid the drift by zeroing the investor's balance before any attribute flip (full-out-transfer or burn → `setAttribute` → re-issue, so each leg of `adjustInvestorsCountsByCountry` fires under a stable attribute), and MASTER can correct existing drift via the `onlyMaster` counter setters at `contracts/compliance/ComplianceServiceRegulated.sol:854-888`.

**Recommended Mitigation:** Reconcile counters inside `setAttribute` before writing the new attribute value. Plumb a hook from `setAttribute` into a new `adjustInvestorCountsAfterAttributeChange` on `ComplianceServiceRegulated`, mirroring the existing `adjustInvestorCountsAfterCountryChange` for the country dimension:

```solidity
function setAttribute(string calldata _id, uint8 _attributeId, uint256 _value, uint256 _expiry, string memory _proofHash) ... {
    require(_attributeId < 16, "Unknown attribute");

    uint256 oldValue = attributes[_id][_attributeId].value;
    bool needsReconcile = (_attributeId == ACCREDITED || _attributeId == QUALIFIED) && (oldValue != _value);
    if (needsReconcile && getToken().balanceOfInvestor(_id) > 0) {
        getComplianceService().adjustInvestorCountsAfterAttributeChange(_id, _attributeId, oldValue, _value);
    }

    attributes[_id][_attributeId].value = _value;
    attributes[_id][_attributeId].expiry = _expiry;
    attributes[_id][_attributeId].proofHash = _proofHash;
    ...
}
```

`adjustInvestorCountsAfterAttributeChange` short-circuits when `balanceOfInvestor(_id) == 0`, otherwise decrements under the OLD flag and increments under the NEW flag. `updateInvestor` inherits the fix because it routes through `setAttribute`.

**Securitize:** Acknowledged.

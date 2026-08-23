---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-29-cyfrin-securitize-full-investor-locks-v2-0-2-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-05-29T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-29-cyfrin-securitize-full-investor-locks-v2-0
title: '`RegistryService::setAttribute` ACCREDITED/QUALIFIED `_expiry` field stored
  but not read by the predicates'
vuln_class: []
---

# `RegistryService::setAttribute` ACCREDITED/QUALIFIED `_expiry` field stored but not read by the predicates

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md)_

---

**Description:** `RegistryService::setAttribute` at `contracts/registry/RegistryService.sol:133-149` writes three fields per attribute: `value`, `expiry`, and `proofHash`. The accreditation/qualification predicate readers (`isAccreditedInvestor` / `isQualifiedInvestor`, both `address` and `string` overloads) read only `value`:

```solidity
function isAccreditedInvestor(string calldata _id) external view override returns (bool) {
    return getAttributeValue(_id, ACCREDITED) == APPROVED;
}
```

No on-chain consumer compares the stored `expiry` against `block.timestamp`. An ACCREDITED attribute set with a 365-day expiry remains effective indefinitely until overwritten by another `setAttribute` call. The field cannot simply be removed: `RegistryService` is UUPS-upgradeable and the `_expiry` slot is part of the on-chain storage layout of every existing attribute record (`AttributeData.value` at slot offset 0, `expiry` at slot offset 1, `proofHash` dynamic-string pointer at slot offset 2). Removing `expiry` from the struct would shift `proofHash`'s slot offset to 1 and corrupt every prior write at upgrade time.

**Files:**

`RegistryService::setAttribute, isAccreditedInvestor, isQualifiedInvestor, getAttributeExpiry`

**Recommended Mitigation:** If `_expiry` is meant to gate on-chain accreditation, add a timestamp check to the four predicate readers:

```solidity
function isAccreditedInvestor(string calldata _id) external view override returns (bool) {
    return getAttributeValue(_id, ACCREDITED) == APPROVED &&
        (getAttributeExpiry(_id, ACCREDITED) == 0 || getAttributeExpiry(_id, ACCREDITED) > block.timestamp);
}
```

The `expiry == 0` carve-out preserves the "no expiry / permanent" semantics for callers who pass `_expiry = 0`. Pair the fix with a counter-reconciliation hook on attribute changes, otherwise an investor's accreditation expiring by timestamp passage will not decrement `accreditedInvestorsCount` / `usAccreditedInvestorsCount` / `euRetailInvestorsCount[country]`.

If `_expiry` is documentary metadata by design (refresh handled off-chain), document the field's role in the function NatSpec and the `IDSRegistryService` interface: "stored but not enforced on-chain; off-chain refresh required for time-bounded enforcement." Keep the storage layout intact regardless of which interpretation applies.


**Securitize:** Acknowledged.

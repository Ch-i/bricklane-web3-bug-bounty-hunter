---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-08-21-tokentable-sui-3-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-08-21T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-08-21-TokenTable-Sui.md
tags:
- firm:codespect
- report:2025-08-21-tokentable-sui
title: '[I-01] Lack of one-time witness may allow objects created in the init(...)
  function to be created after upgrade'
vuln_class: []
---

# [I-01] Lack of one-time witness may allow objects created in the init(...) function to be created after upgrade

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-08-21-TokenTable-Sui.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-08-21-TokenTable-Sui.md)_

---

**Files:** [`ownable.move`](https://github.com/EthSign/ecdsa-token-distributor-sui/tree/5536d80395d269b7d3392b20a924cbcae7a86344/sources/ownable.move#L9), [`fee_collector.move`](https://github.com/EthSign/ecdsa-token-distributor-sui/tree/5536d80395d269b7d3392b20a924cbcae7a86344/sources/fee_collector.move#L44)

**Description:**

For objects that need to ensure global uniqueness, we typically create them in the `init` function because the `init` function is only executed once during package deployment. For example, the `FeeCollectorConfig` object in `fee_collector` and the `OwnerCap` object in `ownable`.

However, since a one-time witness is not used, there is no guarantee that these objects are globally unique. Subsequent upgrades could introduce new functions to create these objects.

**Impact:** `OwnerCap` and `FeeCollectorConfig` may no longer remain globally unique after an upgrade, introducing potential risk such as permission escalation and configuration conflicts.

**Recommendation:** It is recommended to use a one-time witness for objects that need to ensure global uniqueness.

**Status:** Fixed

**Client response:** [Github Commit](https://github.com/EthSign/ecdsa-token-distributor-sui/commit/79fe293de702b9c0542800ad00860b5abd839e5e)

**CODESPECT fix review:** Not fixed. It seems that the `witness` is not actually being used. To ensure the uniqueness of the object, the `witness` should be used in a manner like this.

```move
public struct OWNABLE has drop {}

public struct OwnerCap<phantom T> has key {
    id: UID,
}

fun init(witness: OWNABLE, ctx: &mut TxContext) {
    // The witness proves this is the first and only time this is called
    assert!(sui::types::is_one_time_witness(&witness), 0);

    transfer::transfer(OwnerCap<OWNABLE> {
        id: object::new(ctx),
    }, tx_context::sender(ctx));
}
```

**Client response:** [163eb236b6725a04efb29316c1fe1e7640b7ae31](https://github.com/EthSign/ecdsa-token-distributor-sui/commit/163eb236b6725a04efb29316c1fe1e7640b7ae31)

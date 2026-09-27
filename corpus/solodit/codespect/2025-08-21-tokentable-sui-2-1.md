---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-08-21-tokentable-sui-2-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-08-21T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-08-21-TokenTable-Sui.md
tags:
- firm:codespect
- report:2025-08-21-tokentable-sui
title: '[L-02] The token distributor cannot control distribution parameters and cannot
  withdraw undistributed tokens'
vuln_class: []
---

# [L-02] The token distributor cannot control distribution parameters and cannot withdraw undistributed tokens

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-08-21-TokenTable-Sui.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-08-21-TokenTable-Sui.md)_

---

**Files:** [`base_distributor.move`](https://github.com/EthSign/ecdsa-token-distributor-sui/tree/5536d80395d269b7d3392b20a924cbcae7a86344/sources/base_distributor.move#L85)

**Description:**

The `set_base_params(...)` function sets token distribution parameters, including start and end times, etc. The `withdraw(...)` function is used to claim the tokens that the issuer deposited into the `Distributor`. Both functions can only be called by the project team (`OwnerCap` holder), so the token issuer cannot call them freely. This is inconsistent with implementations on other chains.

```move
public fun set_base_params<T>(
    distributor: &mut Distributor<T>,
    start_time: u64,
    end_time: u64,
    authorized_signer: address,
    _owner_cap: &OwnerCap
) {
    //...
}

public entry fun withdraw<T>(
    distributor: &mut Distributor<T>,
    _owner_cap: &OwnerCap,
    amount: Option<u64>,
    ctx: &mut TxContext
) {
    //...
}
```

**Impact:** This permission restriction reduces the token issuer’s flexibility in distribution, as they cannot freely start or end a distribution nor claim back undistributed tokens on their own.

**Recommendation:** It is recommended to create a permission credential object for each `Distributor`. This object should include a field pointing to the `Distributor` ID to distinguish credentials for different distributors.

**Status:** Fixed

**Client response:** [Github Commit](https://github.com/EthSign/ecdsa-token-distributor-sui/commit/b5205b92c8321be018f2ca3e381f9ac89822fc8f)

**CODESPECT fix review:** It is recommended to set the permission for `set_fee_collector` to `AdminCap`. Although this field currently has no effect, in other versions the `fee_collector` is set by the administrator.

We also noticed that in the new version of the code, a `project_id` is assigned to the distributor. Currently, creating a distributor requires no permission. If a malicious actor were to preemptively occupy a `project_id`, would there be any impact, considering that the permissions of the two functions have now been moved to the creator?

If the `project_id` has a special meaning or purpose and is not randomly generated, and if it is not associated on the backend after the transaction, then it is recommended that the `AdminCap` first assigns the associated `project_id` → creator, and then the creator can create the distributor and freely configure its parameters.

**Client response:**

1. We made another update that eliminates the need to set `fee_collector`. Now all contract calls will all refer to the global `FeeCollectorConfig`. This part is handled by our front-end;
2. `projec_id` has no special meaning so it is fine;

Commit: [b40f93884b1c21d4bcf780f4d06c5964a3b4eca6](https://github.com/EthSign/ecdsa-token-distributor-sui/commit/2ffa820d1809cc3b2d5e3b3cb87cef54537b50f1)

We made another update that requires each distribution to pass in a fee collector reference during creation. Also changed `get_distribution_info` to public entry to facilitate front-end. [3f3f05504e458fee6ce0163673fec0582ca7c3af](https://github.com/EthSign/ecdsa-token-distributor-sui/commit/3f3f05504e458fee6ce0163673fec0582ca7c3af)

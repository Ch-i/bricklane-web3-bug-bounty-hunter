---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-08-21-tokentable-sui-2-0
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
title: '[L-01] The fee collector is optional on Distributor creation, but obligatory
  on claiming leading to temporary DoS'
vuln_class: []
---

# [L-01] The fee collector is optional on Distributor creation, but obligatory on claiming leading to temporary DoS

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-08-21-TokenTable-Sui.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-08-21-TokenTable-Sui.md)_

---

**Files:** [`fungible_token_distributor.move`](https://github.com/EthSign/ecdsa-token-distributor-sui/tree/5536d80395d269b7d3392b20a924cbcae7a86344/sources/fungible_token_distributor.move), [`fungible_token_with_fees_distributor.move`](https://github.com/EthSign/ecdsa-token-distributor-sui/tree/5536d80395d269b7d3392b20a924cbcae7a86344/sources/fungible_token_with_fees_distributor.move), [`base_distributor.move`](https://github.com/EthSign/ecdsa-token-distributor-sui/tree/5536d80395d269b7d3392b20a924cbcae7a86344/sources/base_distributor.move)

**Description:**

Distributors can be created without a fee collector (its an `Option<address>`), however, the claiming routine enforces the existence of such, otherwise the claims revert. This allows for the creation of default broken Distributors, where claiming will not be possible, requiring Owner intervention to set a fee collector in order to restore the Distributor state.

```move
// In claim routine:
assert!(option::is_some(&fee_collector_addr), E_FEE_COLLECTOR_NOT_SET);
[...]
// In the distributor creation:
public fun set_fee_collector<T>(
    distributor: &mut Distributor<T>,
    fee_collector: Option<address>,
    _owner_cap: &OwnerCap
)
```

**Impact:** It is possible to create non-functional distributors which will not allow claiming, leading to partial DoS condition until manual intervention is performed.

**Recommendation:** Enforce setting a fee collector on Distributor creation or allow Distributors without fee collectors (depending on the business needs of the protocol).

**Status:** Fixed

**Client response:** The configuration will be done manually and carefully managed to avoid human error.

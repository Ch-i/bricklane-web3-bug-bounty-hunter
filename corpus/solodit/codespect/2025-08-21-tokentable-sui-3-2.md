---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-08-21-tokentable-sui-3-2
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-08-21T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-08-21-TokenTable-Sui.md
tags:
- firm:codespect
- report:2025-08-21-tokentable-sui
title: '[I-03] Redundant get_distributor_info function calls'
vuln_class: []
---

# [I-03] Redundant get_distributor_info function calls

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-08-21-TokenTable-Sui.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-08-21-TokenTable-Sui.md)_

---

**Original severity:** Best Practices

**Files:** [`fungible_token_distributor.move`](https://github.com/EthSign/ecdsa-token-distributor-sui/tree/5536d80395d269b7d3392b20a924cbcae7a86344/sources/fungible_token_distributor.move#L82), [`fungible_token_distributor.move`](https://github.com/EthSign/ecdsa-token-distributor-sui/tree/5536d80395d269b7d3392b20a924cbcae7a86344/sources/fungible_token_with_fees_distributor.move#L61)

**Description:**

In the `claim(...)` and `claim_with_fees(...)` functions, `get_distributor_info(...)` is called multiple times to retrieve the same data, and the number of redundant calls increases with the number of loop iterations.

```move
public entry fun claim<T, F>(...) {
    let (_, _, _, _, _, paused, _, _, _) = base_distributor::get_distributor_info(distributor);
    //...
    while (i < len) {
        //...
        let (_, authorized_signer, _, _, _, _, _, _, _) = base_distributor::get_distributor_info(distributor);
        //...
    };
    let multiplier = if (delegate_mode) len else 1;
    let (distributor_address, _, _, _, _, _, fee_collector_addr, _, _) =
        base_distributor::get_distributor_info(distributor);
    //...
}

public entry fun claim_with_fees<T, F>(...) {
    let (_, _, _, _, _, paused, _, _, _) = base_distributor::get_distributor_info(distributor);
    //...
    while (i < len) {
        //...
        let (_, authorized_signer, _, _, _, _, _, _, _) = base_distributor::get_distributor_info(distributor);
        //...
    };
    let (_, _, _, _, _, _, fee_collector_addr, _, _) = base_distributor::get_distributor_info(distributor);
    //...
}
```

**Impact:** Such redundant calls increase gas consumption and reduce code readability.

**Recommendation:** It is recommended to retrieve all required variables in a single function call and use them directly in subsequent operations.

**Status:** Fixed

**Client response:** [2f6b14dc43be6cfd664eaa0ff6b884393d1f0898](https://github.com/EthSign/ecdsa-token-distributor-sui/commit/2f6b14dc43be6cfd664eaa0ff6b884393d1f0898)

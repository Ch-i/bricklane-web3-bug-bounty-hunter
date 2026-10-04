---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-08-21-tokentable-sui-3-1
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
title: '[I-02] version string could be a single named constant instead of 2 different
  strings'
vuln_class: []
---

# [I-02] version string could be a single named constant instead of 2 different strings

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-08-21-TokenTable-Sui.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-08-21-TokenTable-Sui.md)_

---

**Files:** [`fee_collector.move`](https://github.com/EthSign/ecdsa-token-distributor-sui/tree/5536d80395d269b7d3392b20a924cbcae7a86344/sources/fee_collector.move#L58), [`ownable.move`](https://github.com/EthSign/ecdsa-token-distributor-sui/tree/5536d80395d269b7d3392b20a924cbcae7a86344/sources/ownable.move#L14)

**Description:**

In both the `fee_collector` and `ownable` modules, the version function uses the same version string (converted via `string::utf8`).

```move
module ecdsa_token_distributor_sui::ownable {
    //...
    public fun version(): String {
        string::utf8(b"0.1.0")
    }
    //...
}

module ecdsa_token_distributor_sui::base_distributor {
    //...
    public fun version(): String {
        string::utf8(b"0.1.0")
    }
    //...
}
```

**Impact:** Defining the same version string in two separate places creates maintenance overhead, as upgrading the version requires modifying two hardcoded instances in the code.

**Recommendation:** It is recommended to optimise this by using a single named constant instead of redundantly defining two separate strings.

**Status:** Fixed

**Client response:** [2f6b14dc43be6cfd664eaa0ff6b884393d1f0898](https://github.com/EthSign/ecdsa-token-distributor-sui/commits/2f6b14dc43be6cfd664eaa0ff6b884393d1f0898)

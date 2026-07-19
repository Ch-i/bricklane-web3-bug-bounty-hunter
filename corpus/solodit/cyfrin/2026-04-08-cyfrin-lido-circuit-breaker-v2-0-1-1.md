---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-08-cyfrin-lido-circuit-breaker-v2-0-1-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-04-08T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-08-cyfrin-lido-circuit-breaker-v2.0.md
tags:
- firm:cyfrin
- report:2026-04-08-cyfrin-lido-circuit-breaker-v2-0
title: Solidity optimizer is not enabled
vuln_class: []
---

# Solidity optimizer is not enabled

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-08-cyfrin-lido-circuit-breaker-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-08-cyfrin-lido-circuit-breaker-v2.0.md)_

---

**Description:** The Foundry configuration does not enable the Solidity optimizer:

```toml
foundry.toml
[profile.default]
src = "src"
out = "out"
libs = ["lib"]
solc = "0.8.34"
```

No `optimizer` or `optimizer_runs` keys are present. Foundry disables the optimizer by default when these are absent. Even at the default 200 runs, the optimizer eliminates dead code, simplifies constant expressions, and reduces both deployment and runtime gas.

**Recommended Mitigation:** Add optimizer settings to `foundry.toml`:

```diff
 [profile.default]
 src = "src"
 out = "out"
 libs = ["lib"]
 solc = "0.8.34"
+optimizer = true
+optimizer_runs = 10000
```

`optimizer_runs` controls the trade-off between deployment cost and runtime call cost. Lower values (e.g., 1) produce smaller bytecode that is cheaper to deploy but slightly more expensive per call. Higher values (e.g., 10,000+) produce larger bytecode optimized for cheaper calls at the cost of more expensive deployment.

Factory-deployed contracts benefit from lower values because deployment cost is paid every time the factory creates a new instance — with hundreds of deployments the cumulative savings outweigh the marginal per-call increase.

Core protocol contracts deployed once but called millions of times benefit from higher values since deployment is a one-time expense. `CircuitBreaker` falls into the latter category — it is deployed once and called repeatedly — so a higher `optimizer_runs` value (e.g., 10,000) is appropriate. The default 200 is a reasonable starting point if unsure.

**Lido:** Fixed in commit [30b01f1](https://github.com/lidofinance/circuit-breaker/commit/30b01f13792e73b4dfc50e4aa093ab4dbf36802a).

**Cyfrin:** Verified.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-3-8
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: Missing zero-value validation for `gas_limit` parameter in both bridges
vuln_class: []
---

# Missing zero-value validation for `gas_limit` parameter in both bridges

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** Both `UpdateGasLimit::handler` functions (and the `executor_gas_limit` parameter in `securitize_bridge::Initialize::handler`) accept a `gas_limit` of 0 without validation. A zero gas limit would cause the executor to fail on the destination chain.

Affected locations:
- `programs/securitize_bridge/src/instructions/admin/update_gas_limit.rs:24`
- `programs/securitize_usdc_bridge/src/instructions/admin/update_gas_limit.rs:21`
- `programs/securitize_bridge/src/instructions/admin/initialize.rs:91`

**Recommended Mitigation:** Add `require_gt!(gas_limit, 0, ...)` checks to prevent accidental zero-value configuration.

**Securitize:** Fixed in [0b5ed9](https://github.com/securitize-io/bc-solana-bridge-sc/commit/0b5ed970244b1b3c7ddb60f0fc454bca34cf5ef8).

Added require_gt!(gas_limit, 0, InvalidGasLimit) guards in both update_gas_limit handlers and in both initialize handlers (DS and USDC bridges), plus a new InvalidGasLimit error variant in each program. CLI now pre-validates the flag and negative tests were added for every call site.

**Cyfrin:** Confirmed.

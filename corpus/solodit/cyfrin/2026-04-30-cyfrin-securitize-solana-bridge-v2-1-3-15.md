---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-3-15
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: Executor quotes must use the same gas limit as on-chain `executor_gas_limit`
vuln_class: []
---

# Executor quotes must use the same gas limit as on-chain `executor_gas_limit`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** Cross-chain relay fees are obtained off-chain from the Wormhole Executor API by sending `relayInstructions` derived from a chosen gas limit.

Both bridge programs always embed `config.executor_gas_limit` when building `relay_instructions` for the on-chain `request_for_execution` CPI.

There is no on-chain check that the caller-supplied signed quote was produced for that same gas limit. `securitize_bridge::initialize` accepts `executor_gas_limit` as an instruction argument, while `securitize_usdc_bridge::initialize` hardcodes `2_000_000` (and other defaults).

```rust
    let config = &mut ctx.accounts.config;

    config.owner = ctx.accounts.owner.key();
    config.usdc_mint = ctx.accounts.usdc_mint.key();
    config.executor_program_id = executor_program_id;
    config.executor_gas_limit = 2_000_000;
    config.max_executor_fee = 0;
    config.max_fee = 0;
    config.min_finality_threshold = 2000;
    config.paused = false;
```


This asymmetry, together with client/SDK defaults, increases the chance that integrators quote with one limit while the program executes with another—typically resulting in failed relay execution or misleading fee estimates, not direct fund theft by a third party.

**Impact:** Mismatched gas between quote and on-chain `relay_instructions` can cause executor CPI or downstream relay to fail.

**Recommended Mitigation:** Always load `executor_gas_limit` from the on-chain bridge config immediately before quoting and bridging.

**Securitize:** Fixed in [db2847e86](https://github.com/securitize-io/bc-solana-bridge-sc/commit/db2847e86a3e9a0ca710e084d29f213baaadcf4e).

Aligned USDC bridge initialize with DS bridge by making executor_gas_limit an explicit instruction argument (removing the hardcoded 2_000_000). SDKs and CLIs already default the quote gas limit to config.executor_gas_limit, so off-chain quoting and on-chain relay instructions are now built from the same field by construction, as recommended.

**Cyfrin:** Confirmed.

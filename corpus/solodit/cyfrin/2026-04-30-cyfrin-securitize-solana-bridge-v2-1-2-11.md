---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-2-11
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: Bridge flows do not implement on-chain rate limiting or cumulative volume caps
vuln_class: []
---

# Bridge flows do not implement on-chain rate limiting or cumulative volume caps

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** **Emergency control is binary pause only.** Both programs gate the main bridge instructions with `!config.paused` and expose `set_paused` to the config `owner` (single-step toggle, no timelock in-program).

`BridgeConfig` carries operational fields (Wormhole addresses, executor, gas limit, finality, pause) but **no** rolling counters, per-window limits, or max-per-transaction beyond what Circle / token balances naturally impose:

```rust
#[account]
#[derive(Default, InitSpace)]
pub struct BridgeConfig {
    pub owner: Pubkey,
    pub wormhole: WormholeAddresses,
    pub batch_id: u32,
    pub finality: u8,

    /// Asset mint managed by the RBAC controller. AssetAccessController PDA is derived from asset_mint.
    pub asset_mint: Pubkey,

    /// RWA RBAC UserRole pubkey. The bridge authority is assigned this role so it can call
    /// revoke_tokens (burn on send) and issue_tokens (mint on receive).
    /// If default (zero), RBAC is not configured and bridge_ds_tokens / execute_vaa_v1 will revert.
    pub authorized_user_role: Pubkey,

    /// Wormhole Executor program id. Default = no Executor.
    pub executor_program_id: Pubkey,

    /// Gas limit for execution on the destination chain (e.g. EVM). Passed in relay instructions
    /// when bridging. Matches EVM gasLimit.
    pub executor_gas_limit: u64,

    /// Emergency pause flag. When true, bridge_ds_tokens and execute_vaa_v1 are disabled.
    pub paused: bool,
    // ...
}
```

**Outbound USDC (`send_usdc_cross_chain_deposit`)** requires a `BridgeCaller` PDA for the signer, but that allowlist does **not** imply any per-slot or per-day budget—only that the pubkey was added by the owner.

Similarly, **outbound DS tokens (`bridge_ds_tokens`)** and **inbound minting (`execute_vaa_v1`)** likewise enforce pause and other checks but introduce **no** protocol-level throttling between successful invocations.

**Impact:** If a **trusted execution path** is compromised or misused, loss can scale with **how fast** transactions can be confirmed and how much liquidity exists, with mitigation depending on **human or off-chain** reaction time to pause.


**Recommended Mitigation:** Consider per-allowlist-signer or global rolling windows (e.g. lamports/USDC base units per epoch).

**Securitize:** Acknowledged; We agree this is a valuable defense-in-depth improvement. Since our EVM bridge has the same gap, we plan to implement rolling rate limits symmetrically on both EVM and Solana in a follow-up release, rather than landing an asymmetric control in this audit cycle.

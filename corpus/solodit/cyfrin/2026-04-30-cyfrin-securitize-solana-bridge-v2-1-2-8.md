---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-2-8
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: Global resolver result PDA can be closed by any BridgeConfig owner
vuln_class: []
---

# Global resolver result PDA can be closed by any BridgeConfig owner

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** The resolver result buffer is a single global PDA derived only from `[RESOLVER_RESULT_ACCOUNT_SEED]`, so it is shared by all bridge instances under the same securitize_bridge program. However, both
  initialization and closure are authorized only through ownership of any BridgeConfig, rather than through a single program-wide admin or a buffer-specific authority.

```34:41:programs/securitize_bridge/src/instructions/admin/init_resolver_result_account.rs
    #[account(
        init,
        payer = owner,
        space = RESOLVER_RESULT_BUFFER_SIZE,
        seeds = [RESOLVER_RESULT_ACCOUNT_SEED],
        bump
    )]
    pub result: Account<'info, ExecutorAccountResolverResult>,
```

`close_resolver_result_account` closes the **same** PDA using only that seed. The instruction still requires `owner` + `config` with `has_one` for **some** `asset_mint`, but the `result` account is **not** constrained to that mint or config:

```28:38:programs/securitize_bridge/src/instructions/admin/close_resolver_result_account.rs
    #[account(
        mut,
        close = receiver,
        seeds = [RESOLVER_RESULT_ACCOUNT_SEED],
        bump
    )]
    pub result: Account<'info, ExecutorAccountResolverResult>,

    /// CHECK: Lamport destination for the closed account. Can be any address.
    #[account(mut)]
    pub receiver: UncheckedAccount<'info>,
```

**Impact:** The owner of one bridge instance can close the shared resolver result PDA and redirect its rent to an arbitrary receiver, temporarily disrupting other bridge instances that rely on the account-backed resolver path for oversized resolution results.

However, impact is limited by the **admin-only** precondition: any **competing or compromised** legitimate bridge `owner` is sufficient and there is no unprivileged exploit path.

**Recommended Mitigation:** If a single global buffer is intentional, **gate** `init` and `close` with a **single** program-level admin PDA or multisig, not merely “any `BridgeConfig.owner`”

**Securitize:** Fixed in [0b2f4fcb](https://github.com/securitize-io/bc-solana-bridge-sc/commit/0b2f4fcb99305dcf9d10771eca0d4eeabd431f01).

**Cyfrin:** Verified.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-2-12
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
title: Concurrent or pipelined resolves last-write-wins
vuln_class: []
---

# Concurrent or pipelined resolves last-write-wins

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** In `handle_resolve_raw`, **Small results** avoid the shared buffer: under `MAX_SOLANA_RETURN_DATA_LEN` (1024 bytes), the program only uses `set_return_data`, which is **per-transaction** and not subject to cross-request overwrite.

However, **Large results** use the global PDA. The PDA address is fixed for the program:

```83:88:programs/securitize_bridge/src/resolver.rs
fn write_resolver_result_to_account<'info>(
    program_id: &Pubkey,
    accounts: &'info [AccountInfo<'info>],
    result_bytes: &[u8],
) -> Result<()> {
    let (result_pda, _) = Pubkey::find_program_address(&[RESOLVER_RESULT_ACCOUNT_SEED], program_id);
```

The account is initialized with the **same** single-seed derivation (no mint or config key in seeds):

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

Each write **overwrites** the discriminator prefix and payload, then zeroes trailing bytes (only to avoid leakage from a **previous longer** payload—not to isolate logical requests):

```173:187:programs/securitize_bridge/src/resolver.rs
    {
        let mut data = result_info.try_borrow_mut_data()?;

        require_gte!(
            data.len(),
            total_len,
            BridgeError::ResolverResultBufferUndersized
        );

        data[..8].copy_from_slice(RESOLVER_RESULT_ACCOUNT);
        data[8..total_len].copy_from_slice(result_bytes);

        // Zero trailing bytes to prevent stale data from a previous larger write.
        data[total_len..].fill(0);
    }
```

There is **no** field storing `vaa_hash`, `emitter_chain`, `sequence`, or `asset_mint` inside this account type for consumers to assert against; correlation is entirely **off-chain** and timing-dependent.

The program comments already acknowledge the split between return data and PDA storage:

```28:30:programs/securitize_bridge/src/resolver.rs
// Solana caps CPI return data at 1024 bytes.
// Larger resolver payloads use `Resolver::Account()` and the executor result PDA.
```

As a result, each successful write **replaces** the entire buffer for that program deployment.
Any off-chain consumer (Wormhole Executor / relayer) that does not **atomically** pair “my resolve transaction” with “read this result” can observe **another** resolve’s output: parallel jobs, retried simulations, or multi-asset deployments on the same program id all contend for the same scratch slot. That is **last-write-wins** semantics with **no on-chain binding** between the account bytes and a specific VAA.

**Impact:** A consumer that reads the PDA **after** another resolve has landed (different VAA, chain, or asset) may build **wrong** remaining accounts or instruction groups for its intended message.

**Recommended Mitigation:** Document that large-resolver mode is **single-flight per program**.

**Securitize**
Fixed in [803df3a](https://github.com/securitize-io/bc-solana-bridge-sc/commit/803df3a884e96427854b4c89da90d8e512c617ec).

**Cyfrin:** Verified.

\clearpage

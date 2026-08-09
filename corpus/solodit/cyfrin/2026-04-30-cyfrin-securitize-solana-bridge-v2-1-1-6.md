---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-30-cyfrin-securitize-solana-bridge-v2-1-1-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-04-30T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-30-cyfrin-securitize-solana-bridge-v2-1
title: '`send_usdc_cross_chain_deposit` hard-couples caller and payer roles, blocking
  OnRamp CPI integration'
vuln_class: []
---

# `send_usdc_cross_chain_deposit` hard-couples caller and payer roles, blocking OnRamp CPI integration

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-30-cyfrin-securitize-solana-bridge-v2.1.md)_

---

**Description:** The USDC bridge send path currently requires a single `payer` signer to simultaneously be:

1. the authorized `BridgeCaller` identity,
2. the owner of the burned USDC token account, and
3. the SOL payer/refund address for executor fees and Circle event-rent flow.


This tight coupling works for direct wallet usage but blocks integrations where roles are intentionally split, **such as the upcoming OnRamp architecture where an OnRamp PDA owns/controls the USDC source account (`caller`) while a separate user wallet funds SOL fees (`payer`). As a result, otherwise valid CPI-based integration patterns are rejected by account constraints before business logic runs.**

```rust
pub struct SendUsdcCrossChainDeposit<'info> {
    #[account(mut)]
    pub payer: Signer<'info>,
```


Error messages reinforce this model (`TokenAccountOwnerMismatch`, `InsufficientPayerLamportsForExecutor`), and there is no alternative account path for “USDC authority/caller != SOL payer.”

**Impact:** The current production path for upcoming OnRamp CPI integration is blocked until role separation is implemented

**Recommended Mitigation:** Decouple identities in the account model and CPI wiring.

**Securitize:** Fixed in [9d3fecf36f2](https://github.com/securitize-io/bc-solana-bridge-sc/commit/9d3fecf36f2e9dc3953defc7d6bd9aaa383e95c8).

Decoupled `payer` and `caller` into two distinct Signer accounts in `send_usdc_cross_chain_deposit`.

Also moved the `config.asset_mint != ZERO_PUBKEY` check from account constraint to handler `require!` in both `bridge_ds_tokens` and `execute_vaa_v1` because Solana flagged `ExecuteVaaV1::try_accounts` for stack-frame overflow under the aggregate constraint load, and relocating the check preserves the invariant guard.

**Cyfrin:** Confirmed.

\clearpage

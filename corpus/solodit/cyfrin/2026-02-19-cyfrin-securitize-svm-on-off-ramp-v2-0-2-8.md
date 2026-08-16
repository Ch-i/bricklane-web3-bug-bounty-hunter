---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0-2-8
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-02-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0
title: Incomplete Rate CPI Context and Understated Minimum NAV Provider Accounts
vuln_class: []
---

# Incomplete Rate CPI Context and Understated Minimum NAV Provider Accounts

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2.0.md)_

---

**Description:** The on-ramp and off-ramp programs invoke NAV provider `rate` instructions via CPI without signing the call with the `on_ramp_authority` or `off_ramp_authority` PDA. The CPI is constructed as an unsigned context:

```rust
let get_rate_ctx = CpiContext::new(
    nav_provider_program.to_account_info(),
    nav_provider_interface::cpi::accounts::Rate {
        asset_mint: asset_mint.to_account_info(),
        nav_provider_state: nav_provider_state.to_account_info(),
    },
)
.with_remaining_accounts(nav_provider_accounts[2..].to_vec());
```

Since the NAV provider program is within the protocol's trust boundary and the admin controls which program is set, this is currently safe. However, if a future NAV provider needs to authenticate the caller (e.g. to restrict rate queries to authorized ramp programs, enforce per-caller rate limits, or distinguish between on-ramp and off-ramp callers for different pricing behavior), the current unsigned CPI pattern would not support this without a protocol upgrade.

The same pattern is used in the off-ramp's `get_rate` and AMM NAV provider paths (`execute_buy_base`, `execute_sell_base`, `quote_buy_base`, `quote_sell_base`), none of which sign with the ramp authority PDA.

**Impact:** NAV provider programs cannot verify the identity of the calling ramp program. While all current NAV providers are within the trust boundary and do not require caller authentication, this limits the extensibility of the NAV provider interface. If a future NAV provider needs to gate access or vary behavior by caller, the interface would need to be updated across both programs.

**Recommended Mitigation:** Sign NAV provider CPI calls with the `on_ramp_authority` / `off_ramp_authority` PDA and include the authority account in the Rate interface struct. This allows NAV providers to optionally verify the caller without requiring it:
```rust
let get_rate_ctx = CpiContext::new_with_signer(
    nav_provider_program.to_account_info(),
    nav_provider_interface::cpi::accounts::Rate {
        asset_mint: asset_mint.to_account_info(),
        nav_provider_state: nav_provider_state.to_account_info(),
        caller_authority: on_ramp_authority.to_account_info(),
    },
    &[&on_ramp_authority_seeds],
)
.with_remaining_accounts(nav_provider_accounts[2..].to_vec());
```

**Securitize:** Fixed in [c8dd8d9](https://github.com/securitize-io/bc-solana-on-off-ramp-sc/commit/c8dd8d9da9a8efe67bf60658e3ec7b8aec7194bd).

**Cyfrin:** Verified.

\clearpage

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-02-cyfrin-securitize-svm-whitelist-acl-support-v2-0-1-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-02-cyfrin-securitize-svm-whitelist-acl-support-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-02-cyfrin-securitize-svm-whitelist-acl-support-v2-0
title: '`Whitelisted` event does not record which freeze-authority path was used'
vuln_class: []
---

# `Whitelisted` event does not record which freeze-authority path was used

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-02-cyfrin-securitize-svm-whitelist-acl-support-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-02-cyfrin-securitize-svm-whitelist-acl-support-v2.0.md)_

---

**Description:** The `whitelist` instruction resolves a `FreezeAuthorityType` before thawing accounts. That enum drives validation, how many `remaining_accounts` are consumed, and which CPI path runs (`token_2022::thaw_account`, access-control `thaw_account`, or SRFC37 `thaw_account`):

> programs/spl-token-whitelist/src/utils/freeze_authority_type.rs
```rs
pub enum FreezeAuthorityType {
    SystemAccount,
    AcProgram,
    AcProgramWithSrfc37,
    SystemAccountWithSrfc37,
}
```

After processing, the program emits `Whitelisted` with only `owner`, `mint`, and `accounts_count`:

> programs/spl-token-whitelist/src/events.rs
```rs
/// Emitted after thawing a batch of token accounts for an owner.
#[event]
pub struct Whitelisted {
    pub owner: Pubkey,
    pub mint: Pubkey,
    pub accounts_count: u8,
}
```


**Impact:**
- The resolved `freeze_authority_type` is not included in the event, preventing off-chain and monitoring systems from knowing the type of thaw/unfreezing that occurred.

**Recommended Mitigation:** We should include the type of `freeze_authority_type` in the event so that we know by which method we unfreezed tokenAccounts

**Securitize:** Acknowledged.

\clearpage

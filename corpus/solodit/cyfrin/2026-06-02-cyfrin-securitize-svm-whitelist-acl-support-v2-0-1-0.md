---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-02-cyfrin-securitize-svm-whitelist-acl-support-v2-0-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-06-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-02-cyfrin-securitize-svm-whitelist-acl-support-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-02-cyfrin-securitize-svm-whitelist-acl-support-v2-0
title: Hardcoded `MINT_CONFIG_DISCRIMINATOR = 1` duplicates upstream TACL state with
  no compile-time tie-back
vuln_class: []
---

# Hardcoded `MINT_CONFIG_DISCRIMINATOR = 1` duplicates upstream TACL state with no compile-time tie-back

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-02-cyfrin-securitize-svm-whitelist-acl-support-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-02-cyfrin-securitize-svm-whitelist-acl-support-v2.0.md)_

---

**Description:** `programs/spl-token-whitelist/src/constants.rs:7` declares `pub const MINT_CONFIG_DISCRIMINATOR: u8 = 1` as a hardcoded literal. The same byte value is the discriminator field on the upstream `spl_token_access_control` (TACL) program's `MintConfig` state struct (which is out of audit scope and not redistributed as a consumable public constant by the upstream crate). The in-scope code re-declares the byte locally and compares the deserialized struct's discriminator against the local literal at `programs/spl-token-whitelist/src/utils/freeze_authority_type.rs:77`:

```rust
require!(
    mint_config.discriminator == MINT_CONFIG_DISCRIMINATOR,
    SplWhitelistErrorCode::InvalidMintConfig
);
```

The discriminator is sourced from upstream state but is not tied back to upstream at compile time. The two values can desynchronize across releases: if the upstream TACL program ever bumps `MintConfig::DISCRIMINATOR` (e.g. to `2` during a struct-layout migration), the in-scope `AcProgramWithSrfc37` and `SystemAccountWithSrfc37` thaw paths will start returning `InvalidMintConfig` for every legitimately-derived `MintConfig` account, silently DoS'ing the sRFC-37 thaw flows until the in-scope program is rebuilt and redeployed with a refreshed literal. The bug surfaces only after the upstream upgrade lands; the in-scope code compiles fine in isolation because the duplicated constant carries no dependency on the upstream definition.

The recoverability question is non-trivial because the program is upgradeable per the deployment context, but the failure mode is silent until users encounter it. A whitelist instruction that previously thawed accounts will start failing for a class of mints that was working a day earlier, with no signal in the in-scope code that explains why.

**Recommended Mitigation:** Two options, in order of preference:

1. Upstream fix - request that `spl_token_access_control` export `MintConfig::DISCRIMINATOR` (or the `MintConfig` discriminator byte) as a `pub const` consumable downstream, then replace the local literal with the imported constant. The Rust compiler will then enforce equality across the workspace via the dependency pin.

2. If upstream cannot be modified, add a build-time or test-time assertion that bridges the gap - e.g. a unit test that constructs a `MintConfig` via the upstream crate's public constructor (or a zeroed instance with the discriminator field set) and asserts the local `MINT_CONFIG_DISCRIMINATOR` equals what the upstream produces. This converts a silent runtime DoS after an upstream upgrade into a build-time failure during dependency bumping, surfacing the drift before deployment.

**Securitize:** Acknowleged.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2-0-1-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-06-26T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2-0
title: Inconsistent `investor_id` length limits across layers (64 vs 256) and an undocumented
  32-byte PDA-seed constraint on the DS path
vuln_class: []
---

# Inconsistent `investor_id` length limits across layers (64 vs 256) and an undocumented 32-byte PDA-seed constraint on the DS path

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md)_

---

**Description:** The `investor_id` field has several different maximum-length limits scattered across the codebase (`64` and `256`), defined under different constant names and enforced at different layers. None of these is a security flaw on its own, but the divergence is a source of confusion and there is an additional, implicit `32`-byte limit on the DS path (PDA seed) that is neither documented nor explicitly validated against the `256`-byte wire limit.


`investor_id` is not defined in a single place. It originates from two different external sources depending on the bridge flow, and is bounded by different constants at each layer:

| Limit | Constant | Location | Layer / meaning |
|-------|----------|----------|-----------------|
| `256` | `MAX_INVESTOR_ID_LEN` | `bc-solana-bridge-sc/programs/securitize_bridge/src/utils/payload.rs:24` | Cross-chain ABI payload (wire format) limit; enforced on encode (`InvestorIdTooLong`) and decode. |
| `64` | `INVESTOR_ID_MAX_LEN` | `bc-solana-bridge-sc/programs/securitize_bridge/src/state/investor_registry.rs:25` | Bridge-side read view of the external SPL `InvestorRegistry`; validates `investor_id.len() <= 64`. |
| `64` | `INVESTOR_ID_MAX_LEN` | `bc-solana-whitelist-sc/programs/spl-token-whitelist/src/constants.rs:14` | On-chain storage cap of the SPL `InvestorRegistry` account (`#[max_len(INVESTOR_ID_MAX_LEN)]`). |
| `32` (implicit) | — (Solana `MAX_SEED_LEN`) | `bc-solana-bridge-sc/programs/securitize_bridge/src/resolver/ds.rs:41-48` | `investor_id` is used as a PDA seed to derive the IMR `Investor` account; Solana hard-caps a single seed at 32 bytes. |

**Impact:** The divergent limits create maintainability/clarity risk: a reader cannot tell from any single constant what the real bound on `investor_id` is.

**Recommended Mitigation:** Consolidate the `investor_id` length limits behind a single, clearly named, shared constant

**Securitize:** Fixed in commits [6fef9983](https://github.com/securitize-io/bc-solana-bridge-sc/commit/6fef9983eed90f43ee96d6420c130c98f1fe68e4) and [26352c4](https://github.com/securitize-io/bc-solana-bridge-sc/commit/26352c4df0fe145debf518000c61f8ec2ca3f89b). We verified that the canonical investor_id is always ≤ 32 bytes, so we consolidated all investor_id length limits to a single value of 32 rather than just renaming: the bridge uses one shared INVESTOR_ID_MAX_LEN = 32 for both the DS-seed check and the SPL InvestorRegistry read-view, and the whitelist storage cap was lowered from 64 to 32. The cross-chain ABI wire bound stays a separate, clearly-named MAX_ENCODED_INVESTOR_ID_LEN = 256 (a deliberately looser envelope). The previously-implicit 32-byte DS PDA-seed limit is now an explicit, named constant with an upfront require!.

**Cyfrin:** Verified.

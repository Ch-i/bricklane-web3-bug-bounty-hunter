---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2-0-2-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-09-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2-0
title: Permissionless `initialize` derives the registrar state and authority PDAs
  from a shared monotonic counter, letting any caller front-run and invalidate pre-signed
  setup transactions
vuln_class: []
---

# Permissionless `initialize` derives the registrar state and authority PDAs from a shared monotonic counter, letting any caller front-run and invalidate pre-signed setup transactions

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md)_

---

**Description:** `initialize` is permissionless: the `Initialize` accounts struct carries no access-control constraint, and `initialize_handler` records `admin` without ever checking the caller. The per-instance `vault_registrar_state` PDA and the `vault_registrar_authority` PDA are both seeded from a single global `vault_registrar_counter` count: the state at `seeds = [VAULT_REGISTRAR_STATE_SEED, vault_registrar_counter.count.to_le_bytes()]` and the authority analogously, with the counter advanced on every call. Because any caller can advance the counter, the address every subsequently pre-derived registrar PDA maps to changes.

**Impact:** A token issuer that reads the counter, derives its registrar PDA, and pre-signs an `initialize` transaction has that transaction rejected the moment anyone else's `initialize` lands first and advances the counter. The issuer loses the submitted transaction fee and must re-read and re-sign; the registrar address is recoverable by re-derivation, but a persistent adversary can deny first-try success repeatedly for only the cost of one extra registrar's rent.

**Recommended Mitigation:** Derive the registrar state and authority PDAs from immutable per-issuer data that an unrelated party cannot front-run. Seeding only with `asset_mint` leaves `initialize` permissionless and lets any caller record themselves as `admin` of the single per-mint registrar, so either gate `initialize` behind an authorized mint-side signer or seed the PDAs with a signer-bound component such as the intended admin plus the mint. Keep the global counter only if clients are documented to derive-and-retry and its advancement is gated so an unrelated party cannot invalidate a pending setup.

**Securitize:** Fixed in [b7ebcf17](https://github.com/securitize-io/bc-solana-whitelister/commit/b7ebcf17fcbaed8c2c3d0a0e4999a6d7e8a512b4) and documented in [99db3ea](https://github.com/securitize-io/bc-solana-whitelister/commit/99db3eae61987a842cd9a99786f074cd53770a1f).

**Cyfrin:** Verified.

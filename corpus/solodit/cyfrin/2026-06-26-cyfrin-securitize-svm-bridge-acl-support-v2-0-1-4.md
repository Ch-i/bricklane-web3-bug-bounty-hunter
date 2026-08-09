---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2-0-1-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-06-26T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2-0
title: Empty `investor_id` can be persisted in `InvestorRegistry` and propagated through
  the SPL bridge
vuln_class: []
---

# Empty `investor_id` can be persisted in `InvestorRegistry` and propagated through the SPL bridge

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md)_

---

**Description:** The SPL whitelist program accepts an empty string as a valid `investor_id` when creating an `InvestorRegistry` PDA. No minimum-length or non-empty check exists on either the admin/freeze-authority `create_investor_registry` path or the user `whitelist` path. Once written, the value is immutable unless the PDA is explicitly deleted. The bridge program reads this field as the compliance source of truth for outbound SPL transfers and embeds it verbatim in the Wormhole payload, so an empty registry entry yields cross-chain messages with no investor attribution.

`InvestorRegistry::new` is the sole validation gate for the stored identifier. It only rejects strings longer than 64 bytes; an empty string (`len == 0`) passes:

```23:27:bc-solana-whitelist-sc/programs/spl-token-whitelist/src/states/investor_registry.rs
    pub fn new(mint: Pubkey, wallet: Pubkey, investor_id: &str, bump: u8) -> Result<Self> {
        require!(
            investor_id.len() <= INVESTOR_ID_MAX_LEN,
            SplWhitelistErrorCode::InvestorIdTooLong
        );
```

**Impact:** Allowing an empty value undermines that invariant: whitelisted wallets can move tokens cross-chain without attaching any investor identifier to the wire payload.

**Recommended Mitigation:** Add an explicit non-empty validation.

**Securitize:** Fixed in commits [91a4db6](https://github.com/securitize-io/bc-solana-whitelist-sc/commit/91a4db613472eecf37cdf468778a48a063ca58f2) and [f3f7d146](https://github.com/securitize-io/bc-solana-bridge-sc/commit/f3f7d1463ce1cfbe0a8c908da60a7f6f8116df5d). The whitelist program's InvestorRegistry::new — the single chokepoint for both the admin/freeze-authority create_investor_registry path and the user whitelist path — now rejects an empty or whitespace-only investor_id (InvestorIdEmpty), so no empty record can be persisted. As defense-in-depth (the bridge and whitelist deploy independently), the bridge's outbound payload encoder (validate_encode_bounds) also rejects an empty/whitespace investor_id before embedding it in the Wormhole payload.

**Cyfrin:** Verified.

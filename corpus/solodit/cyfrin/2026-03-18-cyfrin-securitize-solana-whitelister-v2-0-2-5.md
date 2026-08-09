---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-18-cyfrin-securitize-solana-whitelister-v2-0-2-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-03-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-18-cyfrin-securitize-solana-whitelister-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-18-cyfrin-securitize-solana-whitelister-v2-0
title: Explicitly reject `Pubkey::default()` for `vault_wallet` or the `investor_wallet`
vuln_class: []
---

# Explicitly reject `Pubkey::default()` for `vault_wallet` or the `investor_wallet`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-18-cyfrin-securitize-solana-whitelister-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-18-cyfrin-securitize-solana-whitelister-v2.0.md)_

---

**Description:** EVM implementaion uses `notZeroAddress` for both `vaultAddress` and `investorWalletAddress` as a zero address check. We don’t currently explicitly reject `Pubkey::default()` for `vault_wallet` or the `investor_wallet` in solana implementation. It is advised to add this senity check prior to cpi.

**Impact:** ` vault_wallet` or the `investor_wallet` with default pubkeys can be passed.

**Recommended Mitigation:** Reject default keys when supplied.

**Securitize:** Fixed in [e4f82ff](https://github.com/securitize-io/bc-solana-whitelister/commit/e4f82ff30353e7b9ee58cb57fe918b1dfece524c).

**Cyfrin:** Verifed.

\clearpage

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-05-cyfrin-securitize-evm-async-vault-v2-0-2-8
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-08-05T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-05-cyfrin-securitize-evm-async-vault-v2-0
title: '`AsyncFundVault::totalAssets` reports a mutable liquidity reserve rather than
  total managed assets'
vuln_class: []
---

# `AsyncFundVault::totalAssets` reports a mutable liquidity reserve rather than total managed assets

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md)_

---

**Description:** `AsyncFundVault::totalAssets` returns `reserveBalance`, although this value represents only liquidity currently held by the contract. `MANAGER_ROLE` can increase or decrease it using `AsyncFundVaultAdmin::injectLiquidity` and `AsyncFundVaultAdmin::withdrawReserve` without any corresponding DS Token issuance or burn.

It also includes cancellable deposits and liquidity committed to redemption claims. Therefore, `reserveBalance` represents neither net available liquidity nor the total assets economically backing outstanding DS Tokens issued by vault.

**Impact:** ERC-4626 integrations cannot reliably use `AsyncFundVault::totalAssets` because it reports only the vault’s mutable liquidity reserve, not the total assets backing the DS Token.

**Recommended Mitigation:** Document that the contract is not compatible with integrations relying on ERC-4626 `totalAssets` accounting.

**Securitize:** Fixed in commit [c315a6d](https://github.com/securitize-io/bc-async-ramp-sc/commit/c315a6dd1f013740381c477f6bfbeb169ba4f5ab).

**Cyfrin:** Verified.

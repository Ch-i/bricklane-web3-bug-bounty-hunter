---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-28-cyfrin-securitize-tempo-tip20-v2-0-1-6
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-08-28T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-28-cyfrin-securitize-tempo-tip20-v2-0
title: '`Tip20RegistryService::registerInvestorWithWallets` exceeds Tempo''s transaction
  gas cap'
vuln_class: []
---

# `Tip20RegistryService::registerInvestorWithWallets` exceeds Tempo's transaction gas cap

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md)_

---

**Description:** `Tip20RegistryService::registerInvestorWithWallets` permits a registrar to add up to 100 wallets atomically. For a new investor with a short ID, each wallet creates a `_walletInvestor` slot, an `_investorWallets` element, and a TIP-403 membership slot; `_investorExists` and the array length create two more slots. Registering 100 wallets therefore creates at least 302 slots. Tempo charges 250,000 gas for each new storage slot and caps a transaction at 30 million gas, so storage creation alone requires at least 75.5 million gas before call, loop, event, and calldata costs ([Tempo EVM compatibility documentation](https://tempo.xyz/developers/docs/quickstart/evm-compatibility)).

**Impact:** The documented one-transaction holder-creation flow cannot onboard the maximum supported wallet set on Tempo. A registrar or provider that submits such a request receives an out-of-gas failure even though the input satisfies `MAX_WALLETS_PER_INVESTOR`.

**Recommended Mitigation:** Keep `MAX_WALLETS_PER_INVESTOR` as the total per-investor bound, but add a smaller per-transaction wallet batch limit measured under Tempo's gas schedule. Register the investor first and append larger wallet sets across multiple transactions, or make the provider chunk wallet additions while preserving explicit failure handling.

**Securitize:** Fixed in [PR 19](https://github.com/securitize-io/bc-tempo-sc/pull/19).

**Cyfrin:** Verified.

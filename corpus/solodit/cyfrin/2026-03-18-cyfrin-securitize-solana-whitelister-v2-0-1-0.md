---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-18-cyfrin-securitize-solana-whitelister-v2-0-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-03-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-18-cyfrin-securitize-solana-whitelister-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-18-cyfrin-securitize-solana-whitelister-v2-0
title: Investor's token balance is not checked prior to registration
vuln_class: []
---

# Investor's token balance is not checked prior to registration

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-18-cyfrin-securitize-solana-whitelister-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-18-cyfrin-securitize-solana-whitelister-v2.0.md)_

---

**Description:** The Solana implementation of the `VaultRegistrar` does not enforce the investor token balance check present in the EVM equivalent. In the EVM protocol, the contract verifies that the investor holds the relevant asset (`IERC20(token).balanceOf(investorWalletAddress) > 0`) before allowing the registration of a new vault. The current Solana `register_vault_handler` only checks for the presence of the `existing_investor_wallet` and its identity PDA but fails to verify if the wallet actually holds any tokens of the `asset_mint`.

**Impact:** If the investor doesnt hold tokens it means maybe there is something that has not been complete from KYC or on boarding standpoint, and such investors must be prevented from registration.

**Recommended Mitigation:** Implement the evm equivalent check.

**Securitize:** Fixed in [f16257a](https://github.com/securitize-io/bc-solana-whitelister/commit/f16257a5ab55e5a3252dd2c0b87a3f471614490b).

**Cyfrin:** Verified.

\clearpage

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-05-cyfrin-securitize-evm-async-vault-v2-0-2-5
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-08-05T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-05-cyfrin-securitize-evm-async-vault-v2-0
title: '`AsyncFundVault::withdraw` rejects zero-fill redemption claims'
vuln_class: []
---

# `AsyncFundVault::withdraw` rejects zero-fill redemption claims

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md)_

---

**Description:** A fulfilled redemption with no committed liquidity still has positive claimable shares and must return its unfulfilled DS tokens. `AsyncFundVault::withdraw` instead treats `totalLiquidity == 0` as no claim and reverts, whereas `redeem` checks `totalShares` and can execute the same zero-liquidity claim. See `contracts/AsyncFundVault.sol:708-752` and `contracts/AsyncFundVault.sol:899-955`.

**Impact:** Users and integrations using `withdraw` cannot finalize a zero-fill redemption through that supported claim path. They must switch to `redeem` to recover the escrowed unfulfilled shares.

**Recommended Mitigation:** In `AsyncFundVault::withdraw`, use the same `totalShares` claim-existence check as `redeem`, then retain the exact-assets equality check so a zero-liquidity claim can execute and return unfulfilled shares.

**Securitize:** Fixed in commit [2e2bf00](https://github.com/securitize-io/bc-async-ramp-sc/commit/2e2bf00c39dd60c2f8b7d0e92a79ea234cf4535c).

**Cyfrin:** Verified.

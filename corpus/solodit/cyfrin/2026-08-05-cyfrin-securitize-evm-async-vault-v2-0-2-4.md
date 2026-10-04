---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-05-cyfrin-securitize-evm-async-vault-v2-0-2-4
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
title: '`AsyncFundVault::fulfillRedemptions` burns zero-value redemptions'
vuln_class: []
---

# `AsyncFundVault::fulfillRedemptions` burns zero-value redemptions

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md)_

---

**Description:** For a nonzero pending redemption whose conversion rounds down to zero liquidity, `AsyncFundVault::fulfillRedemptions` enters the branch shared with an empty generation. It sets the fulfillment rate to `WAD`, commits no liquidity, and then burns all pending shares. The fulfilled request can subsequently be cleared without any liquidity payout. See `contracts/AsyncFundVault.sol:649-687`.

**Impact:** A valid nonzero redemption that is below the liquidity token's settlement precision loses its escrowed shares while receiving no liquidity.

**Recommended Mitigation:** Handle a nonzero `totalShares` with zero `totalRedemptionValue` as an unfulfilled redemption: set the fulfillment rate to zero and do not burn the escrowed shares. Alternatively, enforce a redemption minimum guaranteed to produce at least one liquidity-token base unit at settlement.

**Securitize:** Fixed in commit [d7e314f](https://github.com/securitize-io/bc-async-ramp-sc/commit/d7e314f2643569d08c6ab0b959699c96aacd060f).

**Cyfrin:** Verified.

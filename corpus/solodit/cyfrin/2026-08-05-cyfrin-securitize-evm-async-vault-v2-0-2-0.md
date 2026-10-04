---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-05-cyfrin-securitize-evm-async-vault-v2-0-2-0
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
title: '`AsyncFundVault::requestDeposit` rejects documented NonWithdrawable submissions'
vuln_class: []
---

# `AsyncFundVault::requestDeposit` rejects documented NonWithdrawable submissions

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md)_

---

**Description:** `AsyncFundVault::requestDeposit` accepts requests only when the current deposit generation is exactly `GenerationStatus.Active`; the same exact-status check appears in `AsyncFundVault::requestRedeem`. A generation in `NonWithdrawable` therefore rejects new subscription and redemption requests with `NoActiveGeneration`, although that lifecycle state is documented as accepting requests while disallowing cancellations (per `docs/flows.md`). See `contracts/AsyncFundVault.sol:381-385` and `contracts/AsyncFundVault.sol:579-582`.

**Impact:** Investors can be excluded from the documented submission window during normal settlement operations and must wait for a later generation to submit either a subscription or redemption request.

**Recommended Mitigation:** In `AsyncFundVault::requestDeposit` and `requestRedeem`, accept both `Active` and `NonWithdrawable` generations if the documented lifecycle is intended. Keep the Active-only checks in `cancelDepositRequest` and `cancelRedeemRequest`, and account for newly accepted non-cancellable deposits when calculating reserved liquidity.

**Securitize:** Fixed in commit [b239f73](https://github.com/securitize-io/bc-async-ramp-sc/commit/b239f73e65e76689791c2b1ddfabc1a5ad2655f5).

**Cyfrin:** Verified.

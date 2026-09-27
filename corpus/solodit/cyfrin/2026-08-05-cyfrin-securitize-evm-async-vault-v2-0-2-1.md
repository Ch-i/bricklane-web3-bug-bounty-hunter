---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-05-cyfrin-securitize-evm-async-vault-v2-0-2-1
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
title: '`AsyncFundVault::requestDeposit` permits dust griefing of controller capacity'
vuln_class: []
---

# `AsyncFundVault::requestDeposit` permits dust griefing of controller capacity

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md)_

---

**Description:** `AsyncFundVault::requestDeposit` lets an authorized owner create a request for an arbitrary controller and adds the generation to that controller's bounded list before transferring the nominal asset amount. If a fulfilled request converts to zero shares, `deposit` and `mint` reject the claim before clearing that list entry, while `cancelDepositRequest` permits cancellation only for an Active generation. The zero-share condition is reachable when the DS token has materially fewer decimals than the liquidity token, or when the locked NAV is high enough that the smallest deposited asset amount rounds below one DS-token base unit. A third party can therefore create fulfilled, zero-share entries for another controller until the list reaches its capacity. See `contracts/AsyncFundVault.sol:375-400`, `contracts/AsyncFundVault.sol:481-493`, and `contracts/AsyncFundVault.sol:532-559`.

**Impact:** An unconsenting controller can be prevented from creating further deposit requests after dust entries consume its generation-list capacity. The resulting fulfilled entries cannot be cleared through the normal claim or cancellation paths.

**Recommended Mitigation:** Require controller consent when `owner` and `controller` differ, and add a fulfilled zero-share cleanup path that removes the generation entry and refunds its recorded assets. Preserve those refundable fulfilled deposits in reserve-withdrawal accounting until they are claimed or refunded, so a manager cannot withdraw the custody needed by the cleanup path. A settlement-safe minimum request amount can provide an additional guard, but must not replace the cleanup path.

**Securitize:** Fixed in commit [eca80d4](https://github.com/securitize-io/bc-async-ramp-sc/commit/eca80d4c7910e733035e9c88223d8cac14959df6).

**Cyfrin:** Verified.

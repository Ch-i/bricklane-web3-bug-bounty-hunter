---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-05-cyfrin-securitize-evm-async-vault-v2-0-2-3
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
title: '`AsyncFundVault::deposit` strands zero-share fulfilled deposits'
vuln_class: []
---

# `AsyncFundVault::deposit` strands zero-share fulfilled deposits

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md)_

---

**Description:** `AsyncFundVault::deposit` rejects a zero `claimedShares` value before clearing the fulfilled request; `mint` has the same condition. Because `cancelDepositRequest` only accepts an Active generation, the fulfilled assets cannot be refunded through cancellation. This state is reachable when the DS token has materially fewer decimals than the liquidity token, or when the locked NAV is high enough that the fulfilled asset amount rounds below one DS-token base unit. See `contracts/AsyncFundVault.sol:481-493`, `contracts/AsyncFundVault.sol:515-523`, and `contracts/AsyncFundVault.sol:532-559`.

**Impact:** The zero-share fulfilled request has no standalone refund or claim path. If another fulfilled generation later makes the controller's aggregate claim produce nonzero shares, the clear loop consumes the zero-share request as part of the aggregate claim without minting value for that request.

**Recommended Mitigation:** When a fulfilled deposit conversion produces zero shares, clear the request, reduce `reserveBalance`, and return the recorded assets to the controller. Reserve-withdrawal accounting must preserve the refundable amount until the cleanup executes; otherwise a manager can withdraw the custody needed for the refund after fulfillment. Alternatively, enforce a request minimum that is safe under the settlement policy while retaining the refund route when the locked NAV still produces zero shares.

**Securitize:** Fixed in commits [65a7b33](https://github.com/securitize-io/bc-async-ramp-sc/commit/65a7b33d12b180033fc5bf713643c954315d3444), [2208c63](https://github.com/securitize-io/bc-async-ramp-sc/commit/2208c633b9be2a911f441f00d2efcaae12818b49).

**Cyfrin:** Verified.

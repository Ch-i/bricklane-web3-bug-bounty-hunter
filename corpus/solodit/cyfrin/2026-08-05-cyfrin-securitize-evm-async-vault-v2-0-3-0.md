---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-05-cyfrin-securitize-evm-async-vault-v2-0-3-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-08-05T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-05-cyfrin-securitize-evm-async-vault-v2-0
title: '`AsyncFundVault::redeem` permits vault-self claim receivers'
vuln_class: []
---

# `AsyncFundVault::redeem` permits vault-self claim receivers

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md)_

---

**Description:** The claim entry points reject only the zero address, so an authorized controller can select the vault itself as `receiver` in `deposit` or `mint` (contracts/AsyncFundVault.sol:471-523) and in `redeem` or `withdraw` (contracts/AsyncFundVault.sol:708-751). Deposit claims are cleared before DS tokens are issued to that receiver. Redemption claims similarly clear the per-generation state and reduce both `reserveBalance` and `totalClaimableRedemptionLiquidity` before transferring liquidity to the supplied receiver (contracts/AsyncFundVault.sol:906-943). A transfer or issuance to the vault itself leaves the value at the vault while the corresponding claim and accounting obligations have already been cleared.

**Impact:** An authorized controller or approved operator can irreversibly consume the controller's fulfilled claim without delivering usable value to a user-controlled receiver. For redemption claims, the real liquidity balance remains in the vault but the tracked reserve decreases, so later operations may calculate less available liquidity than the vault actually holds. For deposit claims, DS tokens issued to the vault are stranded outside a user's usable redemption flow.

**Recommended Mitigation:** Add a shared receiver validation helper that rejects both the zero address and `address(this)`, then call it in `deposit`, `mint`, `redeem`, and `withdraw` before any claim state is cleared or value is transferred.

**Securitize:** Fixed in commit [629d543](https://github.com/securitize-io/bc-async-ramp-sc/commit/629d543b16927380eb91f3a9b376093c4a2d296f).

**Cyfrin:** Verified.

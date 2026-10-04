---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-05-cyfrin-securitize-evm-async-vault-v2-0-2-2
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
title: '`AsyncFundVault::_executeRedeemClaim` strands redemption rounding dust'
vuln_class: []
---

# `AsyncFundVault::_executeRedeemClaim` strands redemption rounding dust

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md)_

---

**Description:** Redemption settlement locks a generation-level liquidity amount and bulk-burns fulfilled shares, but `_executeRedeemClaim` independently floors each controller's liquidity payout and unfulfilled-share return. It clears each controller's request and decrements the claimable-liquidity counter only by those rounded payouts. Any aggregate remainder consequently has neither a claimant nor a release path: liquidity dust remains reserved, and partial-redemption DS-token dust remains in the vault. See `contracts/AsyncFundVault.sol:679-687` and `contracts/AsyncFundVault.sol:899-955`.

**Impact:** Normal multi-controller redemptions can permanently leave small liquidity balances unavailable to the reserve and unfulfilled DS-token balances unavailable to their controllers. These residual amounts can accumulate across settled generations.

**Recommended Mitigation:** Track each fulfilled generation's remaining liquidity and unfulfilled shares. Decrement those values as claims are processed and allocate each final residual deterministically to the last claimant, or explicitly release a fully settled residual under a documented distribution rule.

**Securitize:** Acknowledged; we're accepting this as-is with no code change, for a few reasons:

* Directionally safe. The dust is unclaimed value sitting in the vault's custody, not a shortfall owed to anyone; it favors the protocol/remaining investors rather than creating any loss.
* Magnitude is immaterial relative to fund operations; bounded to at most (claimants − 1) base units per partial-fill generation, and partial fills themselves are the exception, not the norm.
* Recovery already exists at the right layer. The liquidity-side residual isn't actually stranded; `totalClaimableRedemptionLiquidity` only tracks the true remaining obligation, so once claims settle, the residual becomes ordinary `reserveBalance` headroom recoverable through the existing `withdrawReserve` path. The DS-Token-side residual can be recovered directly by the Issuer/Transfer Agent via the DS Token's own seize/burn functions `(onlyTransferAgentOrAbove / onlyIssuerOrTransferAgentOrAbove)` which operate on any holder, including the vault, with no vault-side involvement required.

Given that, we don't think an ERC-7540-layer admin function is warranted here; it'd duplicate a capability the token layer already provides, for a problem whose value doesn't justify the added surface area.

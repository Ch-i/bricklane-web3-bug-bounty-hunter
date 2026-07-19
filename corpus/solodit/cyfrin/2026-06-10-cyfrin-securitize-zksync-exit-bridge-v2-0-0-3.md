---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2-0-0-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-06-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2-0
title: '`ZKSyncSecuritizeBridge::bridgeDSTokens` enforces only a subset of the destination''s
  issuance compliance, allowing burns that cannot be minted on Ethereum'
vuln_class: []
---

# `ZKSyncSecuritizeBridge::bridgeDSTokens` enforces only a subset of the destination's issuance compliance, allowing burns that cannot be minted on Ethereum

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md)_

---

**Description:** `ZKSyncSecuritizeBridge::bridgeDSTokens` (`contracts/bridge/ZKSyncSecuritizeBridge.sol:113-131`) burns DS tokens after checking only that the caller is a registered wallet and has sufficient *unlocked* balance. Within `_validateLockedTokens` (`:135-152`) `region` is read only to pick a lock period (`(region == US) ? getUSLockPeriod() : getNonUSLockPeriod()`); there is no `region != FORBIDDEN` check. The burn is also unconditional on eligibility, `DSToken.burn` to `validateBurn` to `recordBurn` (`ComplianceServiceRegulated.sol:627`) only adjusts counters, and `getComplianceTransferableTokens` (`:781`) computes only an unlocked-quantity.

The Ethereum mint, triggered by the off-chain relay through the existing Token Issuer, goes through the standard DSToken issuance path: `validateIssuance` (which is `onlyToken`, so it covers any issuance path) calls `preIssuanceCheck` and `require`s a zero code. That gate enforces a range of destination-side eligibility checks:

- destination-wallet registration (code 20)
- `FORBIDDEN` region (code 26)
- liquidate-only (code 90)
- force-accredited (codes 61/62)
- investor-count caps, reading *Ethereum's* counters (code 40)
- regional and global minimum holdings: `minUSTokens` / `minEUTokens` / `minimumHoldingsPerInvestor` (code 51)
- `maximumHoldingsPerInvestor` (code 52)
- the authorized-securities cap (enforced in `validateIssuance`)

On the documented relay path, `TokenIssuer.issueTokens` auto-registers an unregistered destination wallet before issuing, so the whitelist check (code 20) is satisfied there; code 20 only traps a raw `DSToken.issueTokens` to an unregistered wallet. Every destination condition outside "registered + unlocked" is therefore a burn-succeeds-but-mint-reverts trap, reachable via: a country reclassified to `FORBIDDEN` after onboarding; the ZKSync and Ethereum `ComplianceConfigurationService` instances being configured independently with divergent mappings; or the destination-side investor caps (the business-level cross-chain 100-investor limit is enforced per compliance-service instance, so the bridge cannot see Ethereum's counters).

Example: an investor whose country maps to `FORBIDDEN` on Ethereum calls `bridgeDSTokens`; the source checks pass and the tokens are burned; the relay submits the mint to the Token Issuer; `preIssuanceCheck` returns 26 and the mint reverts, the burned value is gone with no on-chain recovery. The same trap occurs on the holdings limits: e.g. a global `minimumHoldingsPerInvestor` of 1000 with a 100-token bridge to a fresh Ethereum wallet (code 51), or a bridge that brings the destination balance to or above `maximumHoldingsPerInvestor` (code 52). The Wormhole `SecuritizeBridge::_validateLockedTokens` (`SecuritizeBridge.sol:567`) shares the same source-side subset logic; on the ZKSync source-only bridge there is no on-chain destination contract, so a rejected mint can only be recovered off-chain.

**Files:**

`ZKSyncSecuritizeBridge::bridgeDSTokens, _validateLockedTokens` (`contracts/bridge/ZKSyncSecuritizeBridge.sol:113-131, 135-152`); also `SecuritizeBridge::_validateLockedTokens` (`contracts/bridge/SecuritizeBridge.sol:567`).

**Impact:** An investor whose destination issuance would be rejected can irreversibly burn tokens on ZKSync that cannot be minted on Ethereum, losing the burned value. The bridge has no on-chain recovery primitive, so remediation is operational. For `FORBIDDEN`/force-accredited/liquidate-only the block typically never clears (effectively permanent); for the investor-cap case the relay may mint later (value stuck rather than lost).

**Recommended Mitigation:** Add source-side pre-burn reverts for the eligibility conditions ZKSync can evaluate against its own services, so consistently-configured cases fail before any burn. All handles are reachable from the existing `dsServiceConsumer`:

```solidity
uint256 internal constant FORBIDDEN = 4; // declare alongside the existing `US = 1`

// in _validateLockedTokens, after computing `region`:
if (region == FORBIDDEN) revert DestinationRestricted();

IDSLockManager lockManager = IDSLockManager(_dsServiceConsumer.getDSService(_dsServiceConsumer.LOCK_MANAGER()));
if (lockManager.isInvestorLiquidateOnly(_investorId)) revert InvestorLiquidateOnly();

if (
    (complianceConfigurationService.getForceAccredited() ||
     (region == US && complianceConfigurationService.getForceAccreditedUS())) &&
    !_registryService.isAccreditedInvestor(_msgSender())
) revert OnlyAccredited();
```

This relies on the ZKSync and Ethereum compliance state being in sync, it reads ZKSync's own config. It only covers the investor-property checks (region, liquidate-only, accreditation); the conditions that read Ethereum balances or counters (investor-count caps, min/max holdings, authorized-securities cap, destination-side registration) cannot be evaluated on the source.

**Securitize:** Tokens in multiple chains must be in sync, if an investor is from a forbidden region/country in zkSync and holds tokens then the burn actually is OK, because we are assuming here that Securitize is failing as a transfer agent and let a forbidden investor hold tokens. Same with accredited.

Liquidation mode is different I think, because we should stopped the burn in that case and revert. We can apply this validation. I think this is also valid for SecuritizeBridge contract, because destination bridge calls issueTokens and trigger same validation.

Fixed in commit [`bfed319`](https://github.com/securitize-io/bc-securitize-bridge-sc/commit/bfed319c0af7d1408aaa7bdc62a93abfec283007)

**Cyfrin:** Liquidate-only verified fixed. FORBIDDEN-region and force-accredited source checks not implemented.


\clearpage

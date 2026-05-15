---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-14-cyfrin-ondo-global-markets-v2-0-1-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-07-14T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-14-cyfrin-ondo-global-markets-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-14-cyfrin-ondo-global-markets-v2-0
title: '`OndoSanityCheckOracle::setAllowedDeviationBps` is not checking zero value
  as input which will introduce problems using it'
vuln_class: []
---

# `OndoSanityCheckOracle::setAllowedDeviationBps` is not checking zero value as input which will introduce problems using it

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-14-cyfrin-ondo-global-markets-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-14-cyfrin-ondo-global-markets-v2.0.md)_

---

**Description:** In `OndoSanityCheckOracle`, there are two types of deviation values: a default deviation applied to all tokens by default, and a token-specific deviation set per asset via `setAllowedDeviationBps()`.

The default deviation value is validated to be non-zero, while token-specific deviations can be set to zero:

[OndoSanityCheckOracle.sol#L222-L245](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/contracts/globalMarkets/tokenManager/sanityCheckOracle/OndoSanityCheckOracle.sol#L222-L245)

```solidity
function setAllowedDeviationBps(...) external onlyRole(CONFIGURER_ROLE) {
  if (bps >= BPS_DENOMINATOR) revert InvalidDeviationBps();
  prices[token].allowedDeviationBps = bps;
  emit AllowedDeviationSet(token, bps);
}

function setDefaultAllowedDeviationBps(...) public onlyRole(CONFIGURER_ROLE) {
  if (bps == 0) revert InvalidDeviationBps(); // enforced here
  if (bps >= BPS_DENOMINATOR) revert InvalidDeviationBps();
  emit DefaultAllowedDeviationSet(defaultDeviationBps, bps);
  defaultDeviationBps = bps;
}
```

Setting a token deviation to zero is functionally meaningless, however, because zero is interpreted as “use the default” during price posting:

[OndoSanityCheckOracle.sol#L189-L192](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/contracts/globalMarkets/tokenManager/sanityCheckOracle/OndoSanityCheckOracle.sol#L189-L192)

```solidity
if (priceData.allowedDeviationBps == 0) {
  priceData.allowedDeviationBps = defaultDeviationBps;
  emit AllowedDeviationSet(token, priceData.allowedDeviationBps);
}
```

This creates a subtle inconsistency: the contract accepts `0` as a valid input for per-token deviations, but the value will be ignored and overridden when posting a price. If zero deviation is considered too strict or unsupported, enforce a `bps > 0` check in `setAllowedDeviationBps()`, mirroring the validation in `setDefaultAllowedDeviationBps()`.

Alternatively, if `0` is meant to indicate “use default,” consider introducing an explicit boolean field to track whether a token’s deviation has been explicitly set, rather than relying on `0` as a sentinel value.

**Ondo:** Fixed in commit [`6a33346`](https://github.com/ondoprotocol/rwa-internal/pull/470/commits/6a333464ee54fe04957331c270ce185a44e5e528)

**Cyfrin:** Verified. `allowedDeviationBps` is not allowed to be 0.

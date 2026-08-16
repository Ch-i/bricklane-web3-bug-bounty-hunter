---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-11-cyfrin-securitize-matchhandler-v2-0-1-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-06-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-11-cyfrin-securitize-matchHandler-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-11-cyfrin-securitize-matchhandler-v2-0
title: Supplied `MatchHandler` deployment flow does not establish required registry
  authorization
vuln_class: []
---

# Supplied `MatchHandler` deployment flow does not establish required registry authorization

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-11-cyfrin-securitize-matchHandler-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-11-cyfrin-securitize-matchHandler-v2.0.md)_

---

**Description:** `MatchHandler::_updateBuyerInRegistry` calls `RegistryService::updateInvestor` from the proxy address on every settlement. In DS Protocol v4.1.0, that function is protected by `onlyExchangeOrAbove`, so the proxy must hold `EXCHANGE`, `ISSUER`, `TRANSFER_AGENT`, or `MASTER` in each token's Trust Service.

```solidity
// contracts/ats/MatchHandler.sol:247
registry.updateInvestor(...); // @audit msg.sender is the MatchHandler proxy

// dstoken/contracts/registry/RegistryService.sol:60
function updateInvestor(...) public override onlyExchangeOrAbove returns (bool) {
```

This authorization does not exist in the current `MatchHandler` deployment flow:

- `ignition/modules/MatchHandler.ts:30-53` only deploys the implementation and proxy and initializes the proxy with the MatchHandler admin, operator, and custodial-wallet addresses. It does not interact with a DS Token's Trust Service.
- `tasks/actions/verify-deployment.ts:15-56` verifies the proxy version, custodial wallet, pause state, and internal MatchHandler role holders, but does not accept a DS Token address or query its Trust Service.


**Impact:** A deployment that follows the documented procedure can be initialized successfully but have every `matchOrder` call revert for a listed DS Token until the external role is granted.

**Recommended Mitigation:** Consider adding a mandatory listing/deployment step that grants the proxy `EXCHANGE`-or-above for every supported DS Token, and extend deployment verification to query the Trust Service role.

Also, document that revoking this external role pauses settlement for the affected token.

**Securitize:** Fixed in commit [`cf4db7a`](https://github.com/securitize-io/bc-ats-sc/commit/cf4db7a5e09a141cd11b7eed24439ea84e594682)

**Cyfrin:** Verified.

\clearpage

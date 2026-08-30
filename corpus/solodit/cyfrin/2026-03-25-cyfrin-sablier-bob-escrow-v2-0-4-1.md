---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-4-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: Missing or inadequate Chainlink Oracle checks in `SablierBob.sol`
vuln_class: []
---

# Missing or inadequate Chainlink Oracle checks in `SablierBob.sol`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** The client's audit onboarding docs indicate that the protocol is intended to be deployed onto L2s and to work with Chainlink Oracles and also non-Chainlink Oracles with a Chainlink-compatible interace.

`SablierBob.sol` uses the `SafeOracle` library however this library omits certain checks as it is designed to not be exclusive to Chainlink Oracles. `SablierBob.sol` does not implement these additional checks, hence it is missing or has inadequate [chainlink oracle checks](https://medium.com/sablier-labs/chainlink-oracle-defi-attacks-93b6cb6541bf):
* no checks for [stale prices](https://medium.com/sablier-labs/chainlink-oracle-defi-attacks-93b6cb6541bf#99af)
* protocol intends to deploy on L2s explicitly Arbitrum & Base but has no checks for [L2 sequencer downtime](https://medium.com/sablier-labs/chainlink-oracle-defi-attacks-93b6cb6541bf#0faf) - when implementing this also [revert](https://solodit.sablier-labs.io/issues/insufficient-checks-to-confirm-the-correct-status-of-the-sequenceruptimefeed-codehawks-zaros-git) if `startedAt == 0`
* no enforcement that returned chainlink price is inside the [aggregator's min/max price](https://medium.com/sablier-labs/chainlink-oracle-defi-attacks-93b6cb6541bf#00ac) - though according to the latest [Chainlink docs](https://docs.chain.link/data-feeds/api-reference#variables-and-functions-in-accesscontrolledoffchainaggregator) the on-chain functions for fetching these are deprecated so consider being able to set them manually

**Sablier:** Acknowledged; while we agree it’s a best practice (and we do have these checks in the Comptroller where no fee is charged if price isn’t updated in 24 hours), adding a staleness check to Bob vaults doesn’t benefit users. Consider:

Case 1: Revet if stale - If the oracle becomes stale and never recovers, users can’t withdraw funds until the end time, even if the target price is reached.

Case 2: Return 0 if stale - same issue as above.

These checks could trap user funds, frustrating those who trust the vault to respect the target price. The only scenario impacted is if the oracle goes stale after hitting the target price → allowing withdrawals even though market price has gone below the target price, but this we believe is acceptable. This benefits users rather than restricting them.

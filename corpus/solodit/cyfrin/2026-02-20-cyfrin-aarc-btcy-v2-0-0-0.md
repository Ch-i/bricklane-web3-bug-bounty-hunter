---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Missing or inadequate Chainlink Oracle checks in `Pricer.sol`
vuln_class: []
---

# Missing or inadequate Chainlink Oracle checks in `Pricer.sol`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** `Pricer.sol` is missing or has inadequate [chainlink oracle checks](https://medium.com/aarc-xyz/chainlink-oracle-defi-attacks-93b6cb6541bf):
* protocol intends to deploy on L2s explicitly Arbitrum & Base but has no checks for [L2 sequencer downtime](https://medium.com/aarc-xyz/chainlink-oracle-defi-attacks-93b6cb6541bf#0faf) - when implementing this also [revert](https://solodit.aarc-xyz.io/issues/insufficient-checks-to-confirm-the-correct-status-of-the-sequenceruptimefeed-codehawks-zaros-git) if `startedAt == 0`
* no enforcement that returned chainlink price is inside the [aggregator's min/max price](https://medium.com/aarc-xyz/chainlink-oracle-defi-attacks-93b6cb6541bf#00ac)

Also consider that the `Pricer` contract currently hard-codes:
* constants related to Chainlink price feed heart-beats
* `CHAINLINK_PRICE_SCALE` which assumes the Chainlink price feed has 8 decimals (as does constant `IBTCYHub::DECIMALS_MULTIPLIER`)

Both of these assumptions are not always true for all Chainlink price feeds. Consider whether these should be configurable parameters or at least when deploying new instances of `Pricer`, verify that these constants are correct for the intended price-feed and modify them if necessary.

Finally also consider [risks of depeg](https://medium.com/aarc-xyz/chainlink-oracle-defi-attacks-93b6cb6541bf#27f9) and whether the protocol needs to detect for a potential depeg event with the intended tokens being used.

**Aarc:** Fixed in [PR10](https://github.com/aarc-xyz/btcy-contracts-main/pull/10).

**Cyfrin:** Verified.

\clearpage

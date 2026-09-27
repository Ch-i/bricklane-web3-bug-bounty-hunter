---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot-3-15
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md
tags:
- firm:codespect
- report:2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot
title: '[I-16] Missing oracle best-practice checks'
vuln_class: []
---

# [I-16] Missing oracle best-practice checks

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md)_

---

**Original severity:** Best Practices

**Files:** [`oracle.py`](https://github.com/SwellNetwork/hlp-internal-be/blob/c650a499023489bfa5d6ac027b28a940a3c44cdc/app/shared/blockchain/oracle/oracle.py#L54)

**Description:**

The bot interacts directly with on-chain oracles to fetch price data used in various calculations. The current implementation of `oracle.py` includes a check for data staleness.

However, if the protocol team decides to switch from the current Redstone oracle to a provider like Chainlink, it is considered best practice to also verify that the returned answer is greater than 0.

Additionally, the current implementation does not consider sequencer downtime, which is relevant in some Layer 2 environments and should be checked to ensure oracle responses are valid and trustworthy.

**Impact:** These are best-practice recommendations and do not currently introduce a direct vulnerability.

**Recommendation:**

- Check that the returned oracle answer is greater than 0;
- Include a check for sequencer downtime;

**Status:** Fixed

**Client response:** Fixed in [83ea2a2c2a1c207ecc166449fc4fab73afef035a](https://github.com/SwellNetwork/hlp-internal-be/commit/83ea2a2c2a1c207ecc166449fc4fab73afef035a). For sequencer downtime checking, currently there’s no sequencer status checker for HyperEVM. Will update when we have it.

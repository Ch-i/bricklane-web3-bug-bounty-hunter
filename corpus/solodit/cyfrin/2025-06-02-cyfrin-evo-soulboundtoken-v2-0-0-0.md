---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-02-cyfrin-evo-soulboundtoken-v2-0-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-06-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md
tags:
- firm:cyfrin
- report:2025-06-02-cyfrin-evo-soulboundtoken-v2-0
title: Missing common Chainlink Oracle validations
vuln_class: []
---

# Missing common Chainlink Oracle validations

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md)_

---

**Description:** The protocol is missing common [Chainlink Oracle validations](https://medium.com/contractlevel/chainlink-oracle-defi-attacks-93b6cb6541bf); it calls `AggregatorV3Interface::latestRoundData` without any validation of the result:
```solidity
function _getLatestPrice() internal view returns (uint256) {
    //slither-disable-next-line unused-return
    (, int256 price,,,) = i_nativeUsdFeed.latestRoundData();
    return uint256(price);
}
```

**Recommended Mitigation:** Implement common Chainlink oracle validations such as checking for:
* [stale prices](https://medium.com/contractlevel/chainlink-oracle-defi-attacks-93b6cb6541bf#99af) using the [correct heartbeat](https://medium.com/contractlevel/chainlink-oracle-defi-attacks-93b6cb6541bf#fb78) for the particular oracle
* [down L2 sequencer](https://medium.com/contractlevel/chainlink-oracle-defi-attacks-93b6cb6541bf#0faf), [revert if `startedAt == 0`](https://solodit.contractlevel.io/issues/insufficient-checks-to-confirm-the-correct-status-of-the-sequenceruptimefeed-codehawks-zaros-git) and potentially a small [grace period](https://docs.chain.link/data-feeds/l2-sequencer-feeds#example-code) of ~2 minutes after it recovers before resuming to fetch price data
* [returned price not at min or max boundaries](https://medium.com/contractlevel/chainlink-oracle-defi-attacks-93b6cb6541bf#00ac)

For this protocol the impact of omitting these checks is quite minimal; in a worst-case scenario users are able to buy NFTs for a cheaper or greater price, but there is no threat to protocol solvency/user liquidation etc as can be a threat in other protocols. And since users can only buy 1 NFT and can't sell/transfer, it isn't that big a deal. If these checks are excluded to keep gas costs down perhaps just put a comment noting this.

**Evo:**
Fixed in commits [6af531e](https://github.com/contractlevel/sbt/commit/6af531e49f7d7dd525da449bcdbdacb171e0c70d),[7a06688](https://github.com/contractlevel/sbt/commit/7a0668860f9b4f43798988349a966147bf94f33f), [93021e4](https://github.com/contractlevel/sbt/commit/93021e4f9c2afb40f64f9f9de69661a134702313).

**Cyfrin:** Verified.

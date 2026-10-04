---
affected_contracts: []
derives_from: []
id: solodit-codespect-2024-12-10-redstone-oracles-1-3
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2024-12-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2024-12-10-RedStone-Oracles.md
tags:
- firm:codespect
- report:2024-12-10-redstone-oracles
title: '[I-04] MAX_DATA_STALENESS Should Vary Based on Data Feed'
vuln_class: []
---

# [I-04] MAX_DATA_STALENESS Should Vary Based on Data Feed

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2024-12-10-RedStone-Oracles.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2024-12-10-RedStone-Oracles.md)_

---

**Files:** [MultiFeedAdapterWithoutRounds.sol](https://github.com/redstone-finance/redstone-oracles-monorepo/blob/ff0f3dcb085f28bd80ddc096825701db6e14d0af/packages/on-chain-relayer/contracts/price-feeds/without-rounds/MultiFeedAdapterWithoutRounds.sol#L31)

**Description:**

The `MAX_DATA_STALENESS` constant defines the maximum duration for which price data is considered valid. Once this period expires, the data is marked as stale, and the oracle will revert rather than return this outdated data. The staleness check is conducted in the following function:

```solidity
function _validateLastUpdateDetailsOnRead(
    bytes32 /* dataFeedId */,
    uint256 /* lastDataTimestamp */,
    uint256 lastBlockTimestamp,
    uint256 lastValue
) internal view virtual returns (bool) {
    return lastValue > 0 && lastBlockTimestamp + MAX_DATA_STALENESS > block.timestamp;
}
```

Since different data feeds have varying update frequencies (heartbeats), the staleness period should also be tailored to each data feed type to ensure accurate and reliable data.

**Recommendation:** Implement dynamic staleness periods for different data feeds to accommodate their specific update frequencies.

**Status:** Acknowledged

**Client response:** This function is virtual and allows the add this logic. However, we wanted to have this param quite high, as for the majority of feeds we can’t predict exact update frequency, as usually it depends on the market volatility.

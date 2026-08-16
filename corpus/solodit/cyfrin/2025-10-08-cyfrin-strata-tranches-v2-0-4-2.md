---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-4-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-10-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-08-cyfrin-strata-tranches-v2-0
title: Missing Validation of Fallback APR Values in `AprPairFeed::latestRoundData`
vuln_class: []
---

# Missing Validation of Fallback APR Values in `AprPairFeed::latestRoundData`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-08-cyfrin-strata-tranches-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md)_

---

**Description:** `AprPairFeed::latestRoundData` fetches APRs from a preferred source (feed or strategy provider). If the feed is stale, it falls back to the strategy provider via `provider.getAprPair()` but does not validate the returned values (e.g., via `ensureValidAprs` or bounds checks), unlike potential validations in the feed path. This allows potentially invalid values to be used

```solidity
function latestRoundData() external view returns (TRound memory) {
        TRound memory round = latestRound;

        if (sourcePref == ESourcePref.Feed) {
            uint256 deltaT = block.timestamp - uint256(round.updatedAt);
            if (deltaT < roundStaleAfter) {
                return round;
            }
            // falls back to strategy ↓
        }

        (int64 aprTarget, int64 aprBase, uint64 t1) = provider.getAprPair();
        return TRound({
            aprTarget: aprTarget,
            aprBase: aprBase,
            updatedAt: t1,
            answeredInRound: latestRoundId + 1
        });
    }
```


**Recommended Mitigation:** Add validation after fallback fetch, similar to feed bounds:
```diff
        (int64 aprTarget, int64 aprBase, uint64 t1) = provider.getAprPair();
+       // Add validation, e.g.:
+       ensureValid(aprTarget);
+       ensureValid(aprBase);
        return TRound({
            aprTarget: aprTarget,
            aprBase: aprBase,
            updatedAt: t1,
            answeredInRound: latestRoundId + 1
        });
```

**Strata:**
Fixed in commit [1c4009a](https://github.com/Strata-Money/contracts-tranches/commit/1c4009a61f6aa1802b0a1541c6e63b096d601d1b) by validating `aprTarget` and `aprBase`.

**Cyfrin:** Verified.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-3-6
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: '`InitializeKarmaTiersScript` doesn''t account for decimals'
vuln_class: []
---

# `InitializeKarmaTiersScript` doesn't account for decimals

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** Script uses raw token amounts as you can see. However Karma token has 18 decimals, therefore all users will have "legendary" tier.
```solidity
contract InitializeKarmaTiersScript is Script {
    function run() external {
        ...

        // Tier 0: 0 karma = 0 tx (no gasless for users without karma)
        tiers[0] = KarmaTiers.Tier({ minKarma: 0, maxKarma: 1, name: "entry", txPerEpoch: 2 });
        tiers[1] = KarmaTiers.Tier({ minKarma: 2, maxKarma: 49, name: "newbie", txPerEpoch: 6 });
        tiers[2] = KarmaTiers.Tier({ minKarma: 50, maxKarma: 499, name: "basic", txPerEpoch: 16 });
        tiers[3] = KarmaTiers.Tier({ minKarma: 500, maxKarma: 4999, name: "active", txPerEpoch: 96 });
        tiers[4] = KarmaTiers.Tier({ minKarma: 5000, maxKarma: 19_999, name: "regular", txPerEpoch: 480 });
        tiers[5] = KarmaTiers.Tier({ minKarma: 20_000, maxKarma: 99_999, name: "power", txPerEpoch: 960 });
        tiers[6] = KarmaTiers.Tier({ minKarma: 100_000, maxKarma: 499_999, name: "pro", txPerEpoch: 10_080 });
        tiers[7] =
            KarmaTiers.Tier({ minKarma: 500_000, maxKarma: 4_999_999, name: "high-throughput", txPerEpoch: 108_000 });
        tiers[8] = KarmaTiers.Tier({ minKarma: 5_000_000, maxKarma: 9_999_999, name: "s-tier", txPerEpoch: 240_000 });
        tiers[9] = KarmaTiers.Tier({
            minKarma: 10_000_000, maxKarma: type(uint256).max, name: "legendary", txPerEpoch: 480_000
        });

        ...
    }
}
```

**Impact:** `KarmaTiers.sol` is initialized with incorrect amounts.

**Recommended Mitigation:** Add e18 notation to token amounts.

**StatusL2:** Fixed in [fa6a44e](https://github.com/status-im/status-network-monorepo/commit/fa6a44ee7abb7cc48168e5d89fb2be85026061cb).

**Cyfrin:** Verified.

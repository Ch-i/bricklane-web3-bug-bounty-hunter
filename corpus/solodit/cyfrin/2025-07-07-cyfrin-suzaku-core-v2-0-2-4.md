---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-2-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-07-07T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-07-cyfrin-suzaku-core-v2-0
title: Missing validation for zero `epochDuration` in AvalancheL1Middleware can break
  epoch based accounting
vuln_class: []
---

# Missing validation for zero `epochDuration` in AvalancheL1Middleware can break epoch based accounting

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-07-cyfrin-suzaku-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md)_

---

**Description:** `AvalancheL1Middleware::EPOCH_DURATION` is an immutable parameter set in the constructor. The current implementation only checks that `slashingWindow` is not less than `epochDuration` but doesn't verify that `epochDuration` itself is greater than zero.

```solidity
constructor(
    AvalancheL1MiddlewareSettings memory settings,
    address owner,
    address primaryAsset,
    uint256 primaryAssetMaxStake,
    uint256 primaryAssetMinStake,
    uint256 primaryAssetWeightScaleFactor
) AssetClassRegistry(owner) {
    // Other validations...

    if (settings.slashingWindow < settings.epochDuration) {
        revert AvalancheL1Middleware__SlashingWindowTooShort(settings.slashingWindow, settings.epochDuration);
    }

    //@audit No check for zero epochDuration!

    START_TIME = Time.timestamp();
    EPOCH_DURATION = settings.epochDuration;
    // Other assignments...
}
```

The check `settings.slashingWindow < settings.epochDuration` will pass as long as slashingWindow is also zero.

**Impact:** Contract functions such as `getEpochAtTs` rely on division by EPOCH_DURATION, which would cause divide-by-zero errors.


**Recommended Mitigation:** Consider adding an explicit validation check for the `epochDuration` parameter in the constructor.

**Suzaku:**
Acknowledged.

**Cyfrin:** Acknowledged.

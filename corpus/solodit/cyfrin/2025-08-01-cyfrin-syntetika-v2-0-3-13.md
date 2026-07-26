---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-3-13
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Not check for timestamp in `distributeYield` could DoS the distribute rewards
vuln_class: []
---

# Not check for timestamp in `distributeYield` could DoS the distribute rewards

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** The `distributeYield()` function in `StakingVault.sol` accepts a timestamp parameter without any validation checks. If an incorrect timestamp is provided (especially one set far in the future), it gets stored as `lastDistributionTimestamp` in the `_updateVestingAmount()` function. This can permanently break the vesting mechanism, as future calls to `distributeYield()` will fail at the `require(getUnvestedAmount() == 0, StillVesting())` check.

```solidity
function _updateVestingAmount(uint256 newVestingAmount, uint256 timestamp) internal {
        require(getUnvestedAmount() == 0, StillVesting()); <-----

        vestingAmount = newVestingAmount;
        lastDistributionTimestamp = timestamp;
    }

```

**Impact:** Permanent denial of service for yield distribution mechanism if the owner set a incorrect timestamp value

**Proof of Concept:** **Recommended Mitigation:**
Check for if the timestamp is less than some threshold in the future.

**Syntetika:**
Acknowledged; users are already trusting the admin to provide yield so it is an even smaller thing to trust the admin to correctly set the `distributeYield` input.

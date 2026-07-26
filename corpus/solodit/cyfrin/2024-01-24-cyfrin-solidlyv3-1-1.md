---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-24-cyfrin-solidlyv3-1-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md
tags:
- firm:cyfrin
- report:2024-01-24-cyfrin-solidlyv3
title: Check for valid pool in `RewardsDistributor::depositLPSolidEmissions`, `depositLPTokenIncentive`
  and `_collectPoolFees`
vuln_class: []
---

# Check for valid pool in `RewardsDistributor::depositLPSolidEmissions`, `depositLPTokenIncentive` and `_collectPoolFees`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-24-cyfrin-solidlyV3.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md)_

---

**Description:** `RewardsDistributor::depositLPSolidEmissions` and `depositLPTokenIncentive` contain no validation that `pool` is a valid pool address, while `depositVoteIncentive` does perform some validation of the pool parameter. Consider adding validation to ensure LP emissions/incentives are recorded against a valid `pool` parameter.

Similarly `RewardsDistributor::_collectPoolFees` never validates if the pool is legitimate and anyone can call its parent function `collectPoolFees`. An attacker could create their own fake pool which implements `ISolidlyV3PoolMinimal::collectProtocol` but doesn't transfer any tokens just returns large output amounts, and for `token0` and `token1` return the address of popular high-profile tokens.

This could make it appear like `RewardsDistributor` has received significantly more rewards than it actually has by corrupting the event log and `periodRewards` storage location with false information. Consider validating the pool in `RewardsDistributor::_collectPoolFees` and potentially whether `RewardsDistributor` has actually received the tokens.

Also note that `RewardsDistributor::periodRewards` is never read in the contract, only written to. If it is not used by off-chain processing then consider removing it.

**Solidly:**
Acknowledged. The off-chain processor only computes pools that are validated through the factory.

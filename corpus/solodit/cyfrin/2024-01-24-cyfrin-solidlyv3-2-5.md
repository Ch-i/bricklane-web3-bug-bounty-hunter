---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-24-cyfrin-solidlyv3-2-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md
tags:
- firm:cyfrin
- report:2024-01-24-cyfrin-solidlyv3
title: Hard-coded pause collateral fee not appropriate for multi-chain usage
vuln_class: []
---

# Hard-coded pause collateral fee not appropriate for multi-chain usage

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-24-cyfrin-solidlyV3.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md)_

---

**Description:** As Solidly aims to be multi-chain in the future, [hard-coding](https://github.com/SolidlyV3/v3-rewards/blob/6dfb435392ffa64652c8f88c98698756ca80cf28/contracts/RewardsDistributor.sol#L553) a pause collateral fee of 5 ether in `RewardsDistributor::pauseClaimsPublic` may not be appropriate on other chains as this amount would represent very little value. Consider having a `public` storage variable for the pause collateral fee and an `onlyOwner` function to set it.

**Solidly:**
Fixed in commit [653c196](https://github.com/SolidlyV3/v3-rewards/commit/653c19659474c93ef0958479191d8103bc7b7e82).

**Cyfrin:**
Verified.

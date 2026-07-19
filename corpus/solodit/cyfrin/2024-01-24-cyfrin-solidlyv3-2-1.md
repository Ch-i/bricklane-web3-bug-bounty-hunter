---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-24-cyfrin-solidlyv3-2-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md
tags:
- firm:cyfrin
- report:2024-01-24-cyfrin-solidlyv3
title: Prefer explicit function for renouncing ownership and 2-step ownership transfer
vuln_class: []
---

# Prefer explicit function for renouncing ownership and 2-step ownership transfer

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-24-cyfrin-solidlyV3.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md)_

---

**Description:** [`RewardsDistributor::setOwner`](https://github.com/SolidlyV3/v3-rewards/blob/6dfb435392ffa64652c8f88c98698756ca80cf28/contracts/RewardsDistributor.sol#L459-L462) and [`SolidlyV3Factory::setOwner`](https://github.com/SolidlyV3/v3-core/blob/callbacks/contracts/SolidlyV3Factory.sol#L60-L64) allow the current owner to brick the ownership by setting `owner = address(0)`, which would prevent future access to admin functionality. Prefer an explicit function for renouncing ownership to prevent this occurring by mistake and prefer a 2-step ownership transfer mechanism. Both of these features are available in OZ [Ownable2Step](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/access/Ownable2Step.sol).

**Solidly:**
Acknowledged.

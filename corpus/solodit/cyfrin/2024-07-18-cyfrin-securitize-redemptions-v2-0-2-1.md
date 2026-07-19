---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-18-cyfrin-securitize-redemptions-v2-0-2-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-07-18T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-18-cyfrin-securitize-redemptions-v2-0
title: No storage gap for upgradeable contract might lead to storage slot collision
vuln_class: []
---

# No storage gap for upgradeable contract might lead to storage slot collision

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-18-cyfrin-securitize-redemptions-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md)_

---

**Description:** For upgradeable contracts, there must be storage gap to "allow developers to freely add new state variables in the future without compromising the storage compatibility with existing deployments" (quote OpenZeppelin). Otherwise it may be very difficult to write new implementation code. Without storage gap, the variable in child contract might be overwritten by the upgraded base contract if new variables are added to the base contract. This could have unintended and very serious consequences to the child contracts, potentially causing loss of user fund or cause the contract to malfunction completely.

Refer to the bottom part of this article: https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable

**Impact:** No storage gap for upgradeable contract might lead to storage slot collision

**Proof of Concept:** Several contracts are intended to be upgradeable contracts in the code base, including

securitize_dev-bc-redemption-sc-32e23d5318be\contracts\utils\BaseContract.sol
securitize_dev-bc-nav-provider-sc-dce942a8a54a\contracts\utils\BaseContract.sol

However, none of these contracts contain storage gap. The storage gap is essential for upgradeable contract because "It allows us to freely add new state variables in the future without compromising the storage compatibility with existing deployments".

**Recommended Mitigation:** Recommend adding appropriate storage gap at the end of upgradeable contracts such as the below. Please reference OpenZeppelin upgradeable contract templates.

```solidity
uint256[50] private __gap;
```
**Securitize:** Fixed in commit [3977ca](https://bitbucket.org/securitize_dev/bc-redemption-sc/commits/3977ca8ffb259a01e8dab894745751cf2150abf4) and [334f49](https://bitbucket.org/securitize_dev/bc-nav-provider-sc/commits/334f4996bc79d0489122210ed54c5596bdcf4eb7)


**Cyfrin:** Verified.

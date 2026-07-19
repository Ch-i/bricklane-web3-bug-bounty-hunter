---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-2-7
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Creation of a new Pod order in place of an existing order requires excess Beans
vuln_class: []
---

# Creation of a new Pod order in place of an existing order requires excess Beans

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

When creating a new Pod order, a user needs to send the Beans required to fulfill the order. If an order already exists with the same sender, `pricePerPod`, `maxPlaceInLine`, and `minFillAmount`, this order must first be canceled, which implies a refund of the previously sent Beans.

One issue with this workflow, which applies to both [v1](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/market/MarketplaceFacet/Order.sol#L62-L68) and [v2](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/market/MarketplaceFacet/Order.sol#L80-L83) orders, is that if the user overrides an existing order, they must send additional Beans because those for the previous order are not considered. Instead, it would make more sense to first cancel the existing order, then try to fulfill the Bean requirement with that of the canceled order, and only if this is not sufficient require the caller send additional Beans.

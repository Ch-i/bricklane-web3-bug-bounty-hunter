---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-2-6
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: '`Listing::getAmountPodsFromFillListing` underflow can lead to undesired behaviour
  of `Listing::_fillListing`'
vuln_class: []
---

# `Listing::getAmountPodsFromFillListing` underflow can lead to undesired behaviour of `Listing::_fillListing`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

If [`fillBeanAmount * 1_000_000 > type(uint256).max`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/market/MarketplaceFacet/Listing.sol#L144), the output of [`Listing::getAmountPodsFromFillListing`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/market/MarketplaceFacet/Listing.sol#L144) would be less than expected, which can lead to the loss of user funds through `Listing::_fillListing`. However, the conditions for this issue to arise are highly unlikely given that `MarketplaceFacet::fillPodListing` is the only function that makes use of this function, and which previously performs a [Bean transfer](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/market/MarketplaceFacet/MarketplaceFacet.sol#L70) of `fillBeanAmount`.  The large number of tokens required to produce the undesired behavior notwithstanding, considering the economic impact, use of `SafeMath` when performing the quoted operation should be considered here.

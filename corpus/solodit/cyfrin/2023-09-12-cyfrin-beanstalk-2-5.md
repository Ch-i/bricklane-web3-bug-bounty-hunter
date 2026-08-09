---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-2-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: When a Pod order is partially filled, the remaining amount pending to fill
  may not be able to be filled
vuln_class: []
---

# When a Pod order is partially filled, the remaining amount pending to fill may not be able to be filled

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

Whenever a Pod order is partially filled, the remaining amount to fill cannot be filled if it is less than the `minFillAmount` set when the order was created. This current behavior forces the creator of the Pod order to cancel the Pod listing, creating a new one with a new `minFillAmount` and applies to both [v1](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/market/MarketplaceFacet/Listing.sol#L191-L200) and [v2](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/market/MarketplaceFacet/Listing.sol#L217-L227) listings.

Depending on the desired behavior:
1. The `minFillAmount` can be decreased to a value lower than/equal to the amount pending to fill.
2. The Pod listing for the remaining amount to fill can be canceled.

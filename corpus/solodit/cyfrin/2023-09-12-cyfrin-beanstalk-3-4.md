---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Additional documentation should be added regarding the correct use of `pricingFunction`
  for v2 Pod listings
vuln_class: []
---

# Additional documentation should be added regarding the correct use of `pricingFunction` for v2 Pod listings

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

When creating a v2 Pod listing, users are required to pass a [pricing function](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/market/MarketplaceFacet/Listing.sol#L91) that will determine the price per Pod depending on the Plot index plus the starting position of Pods inside the Plot and the historical account of harvestable Pods. The difference between these two values yields the [`placeInLine`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/market/MarketplaceFacet/Order.sol#L133) parameter of `Order::_fillPodOrderV2`, which is in units of Pods/Beans and thus has six decimals of precision.

[`LibPolynomial::evaluatePolynomialPiecewise`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/LibPolynomial.sol#L85-L94) evaluates the price per Pod by considering that its parameter `x`, which corresponds to `placeInLine`, has no fixed-point decimals and then executes a third-degree polynomial function depending on the user-supplied `pricingFunction`.

If `x` is considered to have no decimals, then there arises a problem with $placeInLine^{n}$ if $n \neq 1$ given that the number of decimals for each term would increase to $(n -1) \times 6$. This error must, therefore, be handled by the `pricingFunction` bytes, which can be divided into five constituent parameters:
* n (32 bytes): Corresponds to the number of pieces to consider. Each piece consists of a third-degree polynomial.
* breakpoint (32n bytes): `x` values where evaluation changes from one piece to another. There is one breakpoint per piece.
* significands (128n bytes): 4 per piece, ordered from most to least significant term.
* exponents (128n bytes): 4 per piece, ordered from the most to least significant term.
* signs (4n bytes): 4 per piece, indicating the term sign of each piece, ordered from the most to least significant term.

Taking note of the example provided in the [comments of `LibPolynomial`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/LibPolynomial.sol#L21-L45), it can be observed that `x` was intended not to have any additional fixed-point decimals. However, this can be handled through `pricingFunction` with the consideration that the exponents should be defined as follows:
1. The exponent corresponding to the cubic term should be 12 plus the significand decimals. Given that $x$ has 6 decimals, then $x^{3}$ will have 18 decimals. Division by $1 \times 10^{12}$ is necessary to keep the value consistent with the target precision.
2. The exponent corresponding second-degree term should be 6 plus the significand decimals. Given that $x$ has 6 decimals, then $x^{2}$ will have 12 decimals. Division by $1 \times 10^{6}$ is necessary to keep the value consistent with the target precision.

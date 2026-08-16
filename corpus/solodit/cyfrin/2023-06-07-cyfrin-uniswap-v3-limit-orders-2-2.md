---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-07-cyfrin-uniswap-v3-limit-orders-2-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-06-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md
tags:
- firm:cyfrin
- report:2023-06-07-cyfrin-uniswap-v3-limit-orders
title: Validate inputs to `onlyOwner` functions
vuln_class: []
---

# Validate inputs to `onlyOwner` functions

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-07-cyfrin-uniswap-v3-limit-orders.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md)_

---

Whilst there is a comment that states no input validation is performed on inputs to `LimitOrderRegistry::setRegistrar`
and `LimitOrderRegistry::setFastGasFeed` because it is in the owner's best interest to choose valid addresses, it is recommended that some guardrails still be implemented.

For example, to validate the registrar, the contract could call `IKeeperRegistrar::typeAndVersion` and validate that the return value matches that expected in `LimitOrderRegistry::setupLimitOrder` prior to setting it in storage. The `IKeeperRegistrar::register` selector could also be loosely validated by performing a call to this function within a `try/catch` block, passing `address(0)` for the `adminAddress` and catching the `InvalidAdminAddress()` custom error which would indicate expected behaviour.

To validate the fast gas feed, the contract could first make a call to the data feed and check it is reporting correctly within an expected range prior to setting its value in storage.

**GFX Labs:** Acknowledged. This is a valid concern, but in an effort to reduce contract size, these checks will not be added. Also if the owner mistakenly puts in an illogical value, they can simply call the function again with the correct value.

**Cyfrin:** Acknowledged.

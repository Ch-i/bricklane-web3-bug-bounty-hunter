---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-07-01-baton-launchpad-0-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-07-01T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-07-01-Baton%20Launchpad.md
tags:
- firm:pashov-audit-group
- report:2023-07-01-baton-launchpad
title: '[H-01] Missing user input validation can lead to stuck funds'
vuln_class: []
---

# [H-01] Missing user input validation can lead to stuck funds

_Section severity (from Solodit section header): High_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-07-01-Baton Launchpad.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-07-01-Baton%20Launchpad.md)_

---

**Severity**

**Impact:**
High, as all mint fees can be stuck forever

**Likelihood:**
Medium, as users can easily misconfigure inputs

**Description**

There are multiple insufficiencies in the input validation of the arguments of the `initialize` method in `Nft`:

1. The sum of the `supply` of all `categories_` can be less than the `maxMintSupply_` - this would lead to the mint never completing, which results in all of the ETH in the `Nft` contract coming from mints so far being stuck in it forever
2. The `duration` of the `vestingParams_` should have a lower and upper bound as for example a too big of a duration can mean vesting can never complete or a division rounding error
3. The `mintEndTimestamp` of `refundParams_` should not be too further away in the future otherwise refund & vesting mechanisms would never work, and if it is too close then the mint mechanism won't work.

**Recommendations**

Add a validation that the sum of all categories' supply is more than or equal to the `maxMintSupply`. Also add sensible upper and lower bounds for both `duration` for the vesting mechanism and `mintEndTimestamp` for the refund mechanism.

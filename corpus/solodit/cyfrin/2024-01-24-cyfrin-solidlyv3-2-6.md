---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-24-cyfrin-solidlyv3-2-6
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
title: '`RewardsDistributor::_claimSingle` should emit `RewardClaimed` using `amountDelta`'
vuln_class: []
---

# `RewardsDistributor::_claimSingle` should emit `RewardClaimed` using `amountDelta`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-24-cyfrin-solidlyV3.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md)_

---

**Description:** In `RewardsDistributor::_claimSingle`, the `amount` parameter gets subtracted from the `previouslyClaimed` parameter. Consider the case where a user is entitled to 10 reward tokens.

The user claims their 10 tokens.

Then later on the user becomes entitled to another 10 tokens for the same pool/token/type (`rewardKey`). If the user tries to claim with `amount = 10` this would now fail; the user must claim with `amount = 20` to pass the subtraction of the previously claimed amount.

This design seems kind of confusing; users have to keep track of the total amount they have claimed, then add to that the new amount they can claim, and call claim with that total amount.

Even though only the difference `amountDelta` is sent to the user, the `RewardClaimed` event is emitted with `amount`. So in the above scenario there would be two `RewardClaimed` events emitted with `amount (10)` and `amount(20)` even though the user only received 20 total reward tokens.

Consider refactoring this function such that users can simply call it with the amount they are entitled to claim, or at least changing the event emission to use `amountDelta` instead of `amount`.

**Solidly:**
Acknowledged.

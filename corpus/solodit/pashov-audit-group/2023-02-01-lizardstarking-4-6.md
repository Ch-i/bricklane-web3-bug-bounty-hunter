---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-lizardstarking-4-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-lizardstarking
title: '[I-07] Typos, grammatical errors, redundancies and complexity in NatSpec docs
  and comments'
vuln_class: []
---

# [I-07] Typos, grammatical errors, redundancies and complexity in NatSpec docs and comments

_Section severity (from Solodit section header): Informational_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-LizardStarking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md)_

---

There are multiple problems in the NatSpec docs and comments of the `LizardLounge` contract:

- The `IUSDC` file has this `// Unit testing for the LizardLounge Contract` comment, which implies interface is only used for testing but it is used in the `LizardLounge` contract as well
- The NatSpec of `isLizardWithdrawable` says that it checks if a lizard is transferrable but it actually checks if it is withdrawable
- `Checks if the rewards of a lizard for a specific pool has been claimed` -> `Checks if the rewards of a lizard for a specific pool have been claimed`
- Strange comment in `calculateRebasePercentage` - `// Do not times`, should be removed or updated
- Incomplete sentence in the NatSpec of `calculateRebasePercentage` - `@notice We calculate the 1.005^_requiredRebases and`, complete the sentence
- The NatSpec and comments in `calculateRebasePercentage` mention some technical documents but there is no link to them - add it
- Incomplete sentences in the NatSpec of `depositStake` - update it so it is correct
- NatSpec of `depositStake` says `Allows user to deposit their regular Ethlizards for staking` but it allows `Genesis Ethlizards` staking as well, update it
- Typos: `firsts` -> `first`, `depositer` -> `depositor`, `CallerNotDepositer` -> `CallerNotDepositor`, `everytime` -> `every time`
- The NatSpec of `updateGlobalShares` says the method `Gets the current global share counter` which is incorrect, update it so it is correct
- Grammatical errors:
  - `TokenId where share is being calculated` -> `TokenId for which share is being calculated`
  - `Transfer the user the USDC rewards` -> `Transfer the USDC rewards to the user`
  - `If the no pools have been created` -> `If no pools have been created`
  - `after the user is staked` -> `after the user has staked`
  - `// First time stakers mints their...` -> `// First time stakers mint their ...`
  - `A lizard is transferrable if it been over 90 days since it was deposited` -> `A lizard is transferrable if more than 90 days have passed since it was deposited`
  - `... user are protected ...` -> `... users are protected ...`

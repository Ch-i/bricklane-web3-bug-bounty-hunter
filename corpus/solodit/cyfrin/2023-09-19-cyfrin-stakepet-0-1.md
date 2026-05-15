---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-19-cyfrin-stakepet-0-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-09-19T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-stakepet.md
tags:
- firm:cyfrin
- report:2023-09-19-cyfrin-stakepet
title: Inflation attack can cause early users to lose their deposit
vuln_class: []
---

# Inflation attack can cause early users to lose their deposit

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-19-cyfrin-stakepet.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-stakepet.md)_

---

**Severity:** High

**Description:** A malicious `StakePet` contract creator can steal funds from depositors by launching a typical inflation attack. To execute the attack, the creator can first deposit `1 wei` to get `1 wei` of ownership. Creator can subsequently send a big amount of collateral directly to the `StakePet` contract - this will hugely inflate the value of the single share.

Now, all subsequent pet owners who deposit their collateral will get no ownership in return. The `StakePet::ownershipToMint` function uses `StakePet::totalValue` to calculate the ownership of a new depositor. While the total ownership represented by `s_totalOwnership` remains the same `1 wei`, the `totalValueBefore` is a huge number, thanks to a large direct deposit done by the creator. This ensures that the 1 wei of share represents a huge value of collateral & causes the ownership of new depositors to round to 0.

**Impact:** Potential complete loss of funds for new depositors, given they receive no ownership in exchange for their deposited tokens.

**Proof of Concept:**
- Bob, a malicious actor, initiates the StakePet contract.
- By calling `StakePet::create`, Bob creates a pet depositing a mere `1 wei`, which grants him `1 wei` of ownership.
- Bob then directly transfers a significant amount, like 10 ether, to the `StakePet` contract.
- Consequently, a single `1 wei` share becomes equivalent to `10 ether`.
- An innocent user, Pete, tries to create a pet by calling `StakePet::create` and deposits 1 ether.
- Pete, unfortunately, receives zero ownership while his deposit remains within the contract

**Recommended Mitigation:** Inflation attacks have known defences. A comprehensive discussion can be found [here](https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3706).

One noteworthy method, as implemented by Uniswap V2, involves depositing minimal liquidity into the contract and transferring its ownership to a null address, creating "dead shares". This technique protects the subsequent depositor from potential inflation attacks.

In this case, it might be beneficial to introduce a minimum collateral requirement during contract initiation, and accordingly adjust `s_totalOwnership` to match this preset collateral.

**Client:** Fixed in commit [a692abc](https://github.com/Ranama/StakePet/commit/a692abc038fdd8992916f93d213a38c30e3a9764) and [21dd15b](https://github.com/Ranama/StakePet/commit/21dd15b1fceecddb9caf47739b6df1a4d1856367).

**Cyfrin:** Verified.

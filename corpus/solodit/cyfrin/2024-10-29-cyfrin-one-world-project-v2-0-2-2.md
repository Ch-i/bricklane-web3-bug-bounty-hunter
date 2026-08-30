---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-2-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: '`TierConfig::price` is not validated to follow `TierConfig::power` which itself
  is not used or validated'
vuln_class: []
---

# `TierConfig::price` is not validated to follow `TierConfig::power` which itself is not used or validated

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** When creating a new DAO membership, the creator can specify a [`TierConfig::power`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/libraries/MembershipDAOStructs.sol#L34); however, this value is never used or validated and is assumed to be `2` throughout the codebase, for example in `MembershipFactory::upgradeTier` where it is assumed that two lower tier tokens can be burnt for one higher tier token:

```solidity
IMembershipERC1155(daoMembershipAddress).burn(msg.sender, fromTierIndex, 2);
IMembershipERC1155(daoMembershipAddress).mint(msg.sender, fromTierIndex - 1, 1);
```

And in [`MembershipERC1155::shareOf`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/tokens/MembershipERC1155.sol#L165-L176) where the multipliers are hardcoded:

```solidity
function shareOf(address account) public view returns (uint256) {
    return (balanceOf(account, 0) * 64) +
           (balanceOf(account, 1) * 32) +
           (balanceOf(account, 2) * 16) +
           (balanceOf(account, 3) * 8) +
           (balanceOf(account, 4) * 4) +
           (balanceOf(account, 5) * 2) +
           balanceOf(account, 6);
}
```

In addition to this, the `TierConfig::price` is never validated to actually increase with the `TierConfig::power` in both [`MembershipFactory::createNewDAOMembership`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L56) or [`MembershipFactory::updateDAOMembership`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L94):

```solidity
for (uint256 i = 0; i < tierConfigs.length; i++) {
    dao.tiers.push(tierConfigs[i]);
}
```

Therefore, DAOs can be created with prices that do not adhere to either `power` specification. Since the `power` is assumed to be `2` in `MembershipFactory::upgradeTier`, this could result in upgrades being cheaper than intended.

**Impact:** The `power` configuration sent by the DAO creator is not used and assumed to be `2` throughout. `TierConfig::price` is also not validated to actually follow the `power` provided.

**Recommended Mitigation:** Consider using and validating `TierConfig::power` where mentioned above.

**One World Project:** This is acc. To the business logic. The upgradation always takes 2 NFTs from lower tier to mint one higher tier one. The power, among other values, is customizable by the dao creator, but it is kept in contract only for off chain validation and has no direct use in the contract.

**Cyfrin:** Acknowledged.

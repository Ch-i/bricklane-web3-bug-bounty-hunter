---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-2-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: DAOs of all types can be updated with a lower number of tiers and are not validated
  to be above zero
vuln_class: []
---

# DAOs of all types can be updated with a lower number of tiers and are not validated to be above zero

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** When creating a new DAO membership in `MembershipFactory::createNewDAOMembership`, the tiers are [validated](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L60) to be non-zero and not exceed the maximum after parallel data structures are [validated](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L59) to be equal:

```solidity
require(daoConfig.noOfTiers == tierConfigs.length, "Invalid tier input.");
require(daoConfig.noOfTiers > 0 && daoConfig.noOfTiers <= 7, "Invalid tier count.");
```

For `SPONSORED` DAOs, the number of tiers is [validated](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L62-L64) to be equal to the maximum:

```solidity
if (daoConfig.daoType == DAOType.SPONSORED) {
    require(daoConfig.noOfTiers == 7, "Invalid tier count for sponsored.");
}
```

However, there is no such validation when `MembershipFactory::updateDAOMembership` is called, aside from the [cap](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L97) on the number of tiers.

**Impact:** DAOs of all types can be effectively closed by updating the number of tiers to zero.

**Recommended Mitigation:** Consider retaining the original validation if this behavior is not intended, ensuring that the number of tiers remains above zero for all DAOs and that `SPONSORED` DAOs must have the maximum number of tiers.

**One World Project:** Added checks in [`1b05816`](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/commit/1b05816da53ecefa02483141eeef689b331b328d).

**Cyfrin:** Verified. `tiers` is now checked to be `> 0` and if DAO is `SPONSORED` to equal to `7`.

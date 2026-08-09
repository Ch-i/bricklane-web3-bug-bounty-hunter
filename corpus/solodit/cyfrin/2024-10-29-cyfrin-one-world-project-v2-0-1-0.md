---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: DAO name can be stolen by front-running calls to `MembershipFactory::createNewDAOMembership`
vuln_class: []
---

# DAO name can be stolen by front-running calls to `MembershipFactory::createNewDAOMembership`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** When `MembershipFactory::createNewDAOMembership` is called, the newly created `MembershipERC1155` instance it is [associated](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L61) with a name, `ensname`:

```solidity
require(getENSAddress[daoConfig.ensname] == address(0), "DAO already exist.");
```

However, this call can be front-run by a malicious user who sees that another creator is setting up a One World Project membership token and "steals" their name by registering the same name before them.

**Impact:** Anyone can front-run the creation of a DAO membership. This could be used for creating honey pots or just to grief the DAO creator.

**Recommended Mitigation:** Consider validating that the DAO creator is associated with the corresponding ENS name. Alternatively, allow the name to be any string and use a concatenation of the creator and name as a key.

**One World Project:** The DAO name is not necessarily an ENS name, and can be any string. If any name is not available the dao creator is made aware in the frontend website beforehand, and they are free to choose any other name or variation of that name. The name is kept in string format to help the dao creators identify/remember their daos easily without have to remember any ids

If someone is able to create a DAO with that name before you then they are allowed to, and the user would have to choose a different name or variation for their DAO. It is solely up to the DAO creators to decide the DAO names however they like.

**Cyfrin:** Acknowledged.

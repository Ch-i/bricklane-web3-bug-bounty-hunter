---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-3-5
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: Unnecessarily complex `ProxyAdmin` ownership setup
vuln_class: []
---

# Unnecessarily complex `ProxyAdmin` ownership setup

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** The `ProxyAdmin` contract is created in the `MembershipFactory` constructor:

```solidity
constructor(address _currencyManager, address _owpWallet, string memory _baseURI, address _membershipImplementation) {
    // ...
    proxyAdmin = new ProxyAdmin();
```

`ProxyAdmin` inherits `Ownable` and sets the contract owner to `msg.sender`, meaning that this will be the `MembershipFactory` contract.

This ownership structure is further complicated by the requirement for the `EXTERNAL_CALLER` role to call `MembershipFactory::callExternalContract` when managing proxy upgrades. A simpler solution would be to deploy the `ProxyAdmin` independently and pass its address to the `MembershipFactory` constructor.

**Recommended Mitigation:** Consider deploying a separate instance of `ProxyAdmin` and passing its address as a constructor parameter, allowing the ownership structure to be less complex and easier to manage.

**One World Project:** Acknowledged. Intentional. Kept as it is.

**Cyfrin:** Acknowledged.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-3-23
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: '`ComplianceServiceRegulated` and its parent `ComplianceServiceWhitelisted`
  uses a chain of `initializer` modifiers when calling the `initialize`'
vuln_class: []
---

# `ComplianceServiceRegulated` and its parent `ComplianceServiceWhitelisted` uses a chain of `initializer` modifiers when calling the `initialize`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** `ComplianceServiceRegulated` is the child contract inheriting from `ComplianceServiceWhitelisted`.
The `ComplianceServiceRegulated::initialize()` uses the `initializer modifier` as well as the `ComplianceServiceWhitelisted:initialize()`.

```solidity
contract ComplianceServiceRegulated is ComplianceServiceWhitelisted {
    function initialize() public virtual override onlyProxy initializer {
        super.initialize();
    }
}

contract ComplianceServiceWhitelisted is ComplianceService {
    function initialize() public virtual override onlyProxy initializer {
        ComplianceService.initialize();
    }
}
```

According to [OpenZeppelin's documentation](https://docs.openzeppelin.com/contracts/4.x/api/proxy#Initializable-initializer--) and best practices, the initializer modifier should only be used in the final initialization function of an inheritance chain, while initialization functions of parent contracts should use the [onlyInitializing](https://docs.openzeppelin.com/contracts/4.x/api/proxy#Initializable-onlyInitializing--) modifier. This ensures proper initialization when using inheritance.


**Recommended Mitigation:** * change `ComplianceServiceWhitelisted` to have this:
```solidity
contract ComplianceServiceWhitelisted is ComplianceService {

    function initialize() public virtual override onlyProxy initializer {
        _initialize();
    }

    function _initialize() internal onlyInitializing {
        ComplianceService.initialize();
    }
```

* change `ComplianceServiceRegulated` to have this:
```solidity
contract ComplianceServiceRegulated is ComplianceServiceWhitelisted {

    function initialize() public virtual override onlyProxy initializer {
        _initialize();
    }
```

**Securitize:** Fixed in commit [b24ecd5](https://github.com/securitize-io/dstoken/commit/b24ecd57bc82d0fd473d9de1317046300faab984).

**Cyfrin:** Verified.

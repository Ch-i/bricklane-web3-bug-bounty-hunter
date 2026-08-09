---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-4-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Since attribute expiration is deprecated, remove as input parameters, don't
  write it to storage and put comment explaining this
vuln_class: []
---

# Since attribute expiration is deprecated, remove as input parameters, don't write it to storage and put comment explaining this

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** `RegistryService::setAttribute` sets a given `_expiry` field for each attribute at which point the attribute should expire.

However this is never checked anywhere, for example these functions which determine whether a user is accredited or qualified never check the expiry:
```solidity
    function isAccreditedInvestor(string calldata _id) external view override returns (bool) {
        return getAttributeValue(_id, ACCREDITED) == APPROVED;
    }

    function isAccreditedInvestor(address _wallet) external view override returns (bool) {
        string memory investor = investorsWallets[_wallet].owner;
        return getAttributeValue(investor, ACCREDITED) == APPROVED;
    }

    function isQualifiedInvestor(address _wallet) external view override returns (bool) {
        string memory investor = investorsWallets[_wallet].owner;
        return getAttributeValue(investor, QUALIFIED) == APPROVED;
    }

    function isQualifiedInvestor(string calldata _id) external view override returns (bool) {
        return getAttributeValue(_id, QUALIFIED) == APPROVED;
    }
```

Asking the client they have said that attribute expiry is deprecated and not used anywhere, that in practice they are passing zeros for the expiry inputs.

**Recommended Mitigation:** Ideally remove all attribute inputs from functions, however this breaks existing interfaces so is more invasive.

At a minimum change `RegistryService::setAttribute` to never set `attributes[_id][_attributeId].expiry` (leaving it as default zero) and put a comment noting the deprecation in the relevant data store:
```solidity
data-stores/RegistryServiceDataStore.sol
26:        uint256 expiry;
```

**Securitize:** Acknowledged.

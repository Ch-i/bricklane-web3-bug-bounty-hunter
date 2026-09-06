---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-0-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-12-18T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-18-cyfrin-the-standard-auto-redemption-v2-0
title: '`AutoRedemption` mappings are not and can never be populated'
vuln_class: []
---

# `AutoRedemption` mappings are not and can never be populated

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md)_

---

**Description:** The following mappings are declared within the `AutoRedemption` contract:

```solidity
mapping(address => address) hypervisorCollaterals;
mapping(address => bytes) swapPaths;
```

However, they are never populated and there are no public functions capable of doing so either.

When a request is triggered, `lastRequestId` is assigned a non-zero identifier:

```solidity
 lastRequestId = _sendRequest(req.encodeCBOR(), subscriptionID, MAX_REQ_GAS, donID);
```

But the execution of `AutoRedemption::fulfillRequest` will revert due to empty swap paths, so the `lastRequestId` storage will not be reset:

```solidity
bytes memory _collateralToUSDCPath = swapPaths[_token];
...
lastRequestId = bytes32(0);
```

Given the condition within `AutoRedemption::performUpkeep` that there must not be an existing unfulfilled request when creating a new one, this completely blocks all functionality and necessitates a complete redeployment.

**Impact:** Core auto redemption functionality will be broken for all vaults and cannot be fixed without redeployment.

**Recommended Mitigation:** Either:
* Pre-populate the mappings,
* Add access-controlled setter functions, or
* Query state from the `SmartVaultYieldManager` contract.

**The Standard DAO:** Fixed by commit [d72cdce](https://github.com/the-standard/smart-vault/commit/d72cdceed7d60c30abf329e1b8338bb5b13bca2b).

**Cyfrin:** Verified. The setter functions have been added.

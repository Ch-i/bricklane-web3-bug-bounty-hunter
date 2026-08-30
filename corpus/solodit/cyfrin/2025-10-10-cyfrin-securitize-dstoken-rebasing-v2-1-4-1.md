---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-4-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Cache result of identical external calls when the result can't change
vuln_class: []
---

# Cache result of identical external calls when the result can't change

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** Cache result of identical external calls when the result can't change.

* `contracts/service/ServiceConsumer.sol`
```solidity
// in the modifiers, cache `trustManager.getRole(msg.sender)` and
// use the cached value inside the `require` statements
59:        require(trustManager.getRole(msg.sender) == ROLE_TRANSFER_AGENT || trustManager.getRole(msg.sender) == ROLE_ISSUER || trustManager.getRole(msg.sender) == ROLE_MASTER, "Insufficient trust level");
65:        require(trustManager.getRole(msg.sender) == ROLE_ISSUER || trustManager.getRole(msg.sender) == ROLE_MASTER, "Insufficient trust level");
71:        require(trustManager.getRole(msg.sender) == ROLE_TRANSFER_AGENT || trustManager.getRole(msg.sender) == ROLE_MASTER, "Insufficient trust level");
77:        require(
78:            trustManager.getRole(msg.sender) == ROLE_EXCHANGE
79:            || trustManager.getRole(msg.sender) == ROLE_ISSUER
80:            || trustManager.getRole(msg.sender) == ROLE_TRANSFER_AGENT
81:            || trustManager.getRole(msg.sender) == ROLE_MASTER,
100:            require(trustManager.getRole(msg.sender) == ROLE_ISSUER || trustManager.getRole(msg.sender) == ROLE_MASTER, "Insufficient trust level");
108:            require(trustManager.getRole(msg.sender) == ROLE_TRANSFER_AGENT || trustManager.getRole(msg.sender) == ROLE_MASTER, "Insufficient trust level");
116:            require(trustManager.getRole(msg.sender) == ROLE_ISSUER || trustManager.getRole(msg.sender) == ROLE_MASTER, "Insufficient trust level");
```

* `contracts/swap/SecuritizeSwap.sol`
```solidity
// cache `navProvider.rate` in `buy`, also change `calculateStableCoinAmount` to take the rate
// as an input to save another call inside it
L132:        require(navProvider.rate() > 0, "NAV Rate must be greater than 0");
L141:        emit Buy(msg.sender, _dsTokenAmount, stableCoinAmount, navProvider.rate());
L240:        return _dsTokenAmount * navProvider.rate() / (10 ** ERC20(address(dsToken)).decimals());
```

* `contracts/compliance/ComplianceServiceRegulated.sol`
```solidity
// cache these two external calls in `getUSInvestorsLimit`
103:        if (compConfService.getMaxUSInvestorsPercentage() == 0) {
107:        if (compConfService.getUSInvestorsLimit() == 0) {

// cache `getInvestor(_to)` in `preIssuanceCheck`
420:        string memory toCountry = IDSRegistryService(_services[REGISTRY_SERVICE]).getCountry(IDSRegistryService(_services[REGISTRY_SERVICE]).getInvestor(_to));
431:        if (IDSLockManager(_services[LOCK_MANAGER]).isInvestorLiquidateOnly(IDSRegistryService(_services[REGISTRY_SERVICE]).getInvestor(_to))) {
```

**Securitize:** Acknowledged.

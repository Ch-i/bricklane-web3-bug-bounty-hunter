---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-4-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Cache storage to prevent identical storage reads
vuln_class: []
---

# Cache storage to prevent identical storage reads

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** Reading from storage is expensive; cache storage to prevent identical storage reads:

* `contracts/registry/RegistryService.sol`:
```solidity
// cache `getInvestor(_address)` in `getInvestorDetails`
206:        return (getInvestor(_address), getCountry(getInvestor(_address)));
```

* `contracts/issuance/TokenIssuer.sol`
```solidity
// cache `getRegistryService()` in `issueTokens` and `registerInvestor`
44:        if (getRegistryService().isWallet(_to)) {
45:            require(CommonUtils.isEqualString(getRegistryService().getInvestor(_to), _id), "Wallet does not belong to investor");
63:        if (!getRegistryService().isInvestor(_id)) {
64:            getRegistryService().registerInvestor(_id, _collisionHash);
65:            getRegistryService().setCountry(_id, _country);
69:                getRegistryService().setAttribute(_id, KYC_APPROVED, _attributeValues[0], _attributeExpirations[0], "");
70:                getRegistryService().setAttribute(_id, ACCREDITED, _attributeValues[1], _attributeExpirations[1], "");
71:                getRegistryService().setAttribute(_id, QUALIFIED, _attributeValues[2], _attributeExpirations[2], "");
```

* `contracts/token/TokenLibrary.sol`
```solidity
// cache `supportedFeatures.value` in `setFeature`
62:        if (enable && (supportedFeatures.value & mask == 0)) {
63:            supportedFeatures.value = supportedFeatures.value ^ mask;
64:        } else if (!enable && (supportedFeatures.value & mask >= 1)) {
65:            supportedFeatures.value = supportedFeatures.value ^ mask;

// This function can also delete the `base` variable since it is hard-coded and
// only used once so no point to it.
```

* `contracts/token/StandardToken.sol`
```solidity
// cache `allowances[msg.sender][_spender] + _addedValue` then use it
// when writing storage and emitting event. Do something similar in `decreaseApproval`
// to avoid re-reading storage when emitting the event
128:        allowances[msg.sender][_spender] = allowances[msg.sender][_spender] + _addedValue;
129:        emit Approval(msg.sender, _spender, allowances[msg.sender][_spender]);
```

* `contracts/trust/TrustService.sol`
```solidity
// cache `roles[msg.sender]` in modifiers
70:        require(roles[msg.sender] == MASTER || roles[msg.sender] == ISSUER, "Not enough permissions");
86:        if (roles[msg.sender] != MASTER) {
87:            if (roles[msg.sender] == ISSUER) {
90:                require(roles[msg.sender] == _role, "Not enough permissions. Only same role allowed");
100:        if (roles[msg.sender] != MASTER) {
102:            if (roles[msg.sender] == ISSUER) {
105:                require(roles[msg.sender] == role, "Not enough permissions. Only same role allowed");

// cache `roles[msg.sender]` and `ownersEntities[msg.sender]` in `onlyEntityOwnerOrAbove`
// ideally here perform the `roles[msg.sender]` checks first and only perform the `ownersEntities[msg.sender]`
// afterwards if required
113:            roles[msg.sender] == MASTER ||
114:                roles[msg.sender] == ISSUER ||
115:                (!CommonUtils.isEmptyString(ownersEntities[msg.sender]) &&
116:                  CommonUtils.isEqualString(ownersEntities[msg.sender], _name)),

// cache `ownersEntities[_owner]` in `onlyExistingEntityOwner`
140:            !CommonUtils.isEmptyString(ownersEntities[_owner]) &&
141:            CommonUtils.isEqualString(ownersEntities[_owner], _name),

// cache `operatorsEntities[_operator]` in `onlyExistingOperator`
154:            !CommonUtils.isEmptyString(operatorsEntities[_operator]) &&
155:            CommonUtils.isEqualString(operatorsEntities[_operator], _name),

// cache `resourcesEntities[_resource]` in `onlyExistingResource`
168:            !CommonUtils.isEmptyString(resourcesEntities[_resource]) &&
169:           CommonUtils.isEqualString(resourcesEntities[_resource], _name),
```

* `contracts/swap/SecuritizeSwap.sol`
```solidity
// cache `IDSRegistryService(getDSService(REGISTRY_SERVICE))` in `swap`
// pass it in as a parameter to `_registerNewInvestor` to save another identical storage read
103:        if (!IDSRegistryService(getDSService(REGISTRY_SERVICE)).isInvestor(_senderInvestorId)) {
114:        string memory investorWithNewWallet = IDSRegistryService(getDSService(REGISTRY_SERVICE)).getInvestor(_newInvestorWallet);
116:            IDSRegistryService(getDSService(REGISTRY_SERVICE)).addWallet(_newInvestorWallet, _senderInvestorId);
214:        IDSRegistryService registryService = IDSRegistryService(getDSService(REGISTRY_SERVICE));

// cache `USDCBridge` and `bridgeChainId` in `executeStableCoinTransfer`
// a more optimized implementation looks like this:
function executeStableCoinTransfer(address from, uint256 value) private {
    // 1 SLOAD since both stored in the same slot
    (IUSDCBridge USDCBridgeCache, uint16 bridgeChainIdCache) = (USDCBridge, bridgeChainId);

    if (bridgeChainIdCache != 0 && address(USDCBridgeCache) != address(0)) {
        stableCoinToken.transferFrom(from, address(this), value);
        stableCoinToken.approve(address(USDCBridgeCache), value);
        USDCBridgeCache.sendUSDCCrossChainDeposit(bridgeChainIdCache, issuerWallet, value);
    } else {
        stableCoinToken.transferFrom(from, issuerWallet, value);
    }
}
```

* `contracts/compliance/ComplianceServiceWhitelisted.sol`
```solidity
// cache `getToken()` in `preTransferCheck`
50:        return doPreTransferCheckWhitelisted(_from, _to, _value, getToken().balanceOf(_from), getToken().isPaused());
```

* `contracts/compliance/ComplianceServiceRegulated.sol`
```solidity
// cache `getRegistryService()` and `getComplianceConfigurationService()` in `recordTransfer`
// ideally these would be cached upstream and passed down to functions such as `recordTransfer`
// that need them
800:        string memory investor = getRegistryService().getInvestor(_who);
801:        string memory country = getRegistryService().getCountry(investor);

803:        uint256 region = getComplianceConfigurationService().getCountryCompliance(country);
807:            lockTime = getComplianceConfigurationService().getUSLockPeriod();
809:            lockTime = getComplianceConfigurationService().getNonUSLockPeriod();
```

**Securitize:** Acknowledged.

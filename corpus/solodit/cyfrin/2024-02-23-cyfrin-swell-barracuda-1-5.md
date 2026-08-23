---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-1-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-02-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
tags:
- firm:cyfrin
- report:2024-02-23-cyfrin-swell-barracuda
title: '`NodeOperatorRegistry::updateOperatorControllingAddress` allows to override
  `_newOperatorAddress` if its address is already assigned to an operator ID'
vuln_class: []
---

# `NodeOperatorRegistry::updateOperatorControllingAddress` allows to override `_newOperatorAddress` if its address is already assigned to an operator ID

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-02-23-cyfrin-swell-barracuda.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md)_

---

**Description:** Current implementation does not check if the new assigned address has already been assigned to an operator ID. As a consequence, its current value can be over written in mapping `getOperatorIdForAddress`, and `getOperatorForOperatorId` will have 2 operator IDs pointing to the same operator.

The direct consequences of this are on `_getOperatorSafe` and `_getOperatorIdSafe`, which will only return data for the new assigned operator ID.

Therefore:
* `NodeOperatorRegistry::getOperatorsPendingValidatorDetails` won't be able to return old `_newOperatorAddress` associated validators details
* `NodeOperatorRegistry::getOperatorsActiveValidatorDetails` won't be able to return old `_newOperatorAddress` associated active validators details
* `enableOperator` won't be able to enable old operator record
* **__`disableOperator` won't be able to disable old operator record__**.  This can affect function `usePubKeysForValidatorSetup` given that the protocol won't be able to disable already enabled public key to be used for validator setup given that there is no way to modify previous `getOperatorForOperatorId[_newOperatorAddress].enabled` storage and [force the function to revert](https://github.com/SwellNetwork/v3-contracts-lst/blob/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/NodeOperatorRegistry.sol#L194-L196). Given that the only one allowed to call the function is the BOT by previously calling `DepositManager::setupValidators` the impact is limited.
* `updateOperatorRewardAddress` won't be able to modify reward address from old operator record
* `updateOperatorName` won't be able to modify name from old operator record

This issue has not been introduced in the new changes but is in the mainnet [code](https://github.com/SwellNetwork/v3-core-public/blob/master/contracts/lst/contracts/implementations/NodeOperatorRegistry.sol#L348-L364).

**Proof Of Concept:**
Add the following test to `updateOperatorFields.test.ts`:
```typescript
    it("Should revert updating operator controlling address to existing address", async () => {
      // create another operator
      await NodeOperatorRegistry_Deployer.addOperator(
        "OPERATOR_2",
        NewOperator.address,
        NewOperator.address
      );

      // attempt to update first operator's controlling address to be
      // the same as the newly created operator - should revert but doesn't
      await NodeOperatorRegistry_Deployer.updateOperatorControllingAddress(
        Operator.address,
        NewOperator.address
      );
    });
```

**Recommended mitigation:**
Check that `_newOperatorAddress` is not already assigned to an operator (similar to `addOperator` which [already does this](https://github.com/SwellNetwork/v3-contracts-lst/blob/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/NodeOperatorRegistry.sol#L300-L302), may wish to create a new private or public function for code reuse):
```diff
  function updateOperatorControllingAddress(
    address _operatorAddress,
    address _newOperatorAddress
  )
    external
    override
    checkRole(SwellLib.PLATFORM_ADMIN)
    checkZeroAddress(_newOperatorAddress)
  {

    if (_operatorAddress == _newOperatorAddress) {
        revert CannotSetOperatorControllingAddressToSameAddress();
    }
+   if(getOperatorIdForAddress[_newOperatorAddress] != 0){
+       revert CannotUpdateOperatorControllingAddressToAlreadyAssignedAddress();
+   }

    uint128 operatorId = _getOperatorIdSafe(_operatorAddress);

    getOperatorIdForAddress[_newOperatorAddress] = operatorId;
    getOperatorForOperatorId[operatorId]
      .controllingAddress = _newOperatorAddress;

    delete getOperatorIdForAddress[_operatorAddress];
  }
```

**Swell:** Fixed in commit [55c7d5f](https://github.com/SwellNetwork/v3-contracts-lst/commit/55c7d5fba6d55c68558dcd15de016927e07e38fd).

**Cyfrin:**
Verified.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-2-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-07-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-10-cyfrin-casimir-v2-0
title: Reporter trying to reshare a pending validator will lead to denial of service
vuln_class: []
---

# Reporter trying to reshare a pending validator will lead to denial of service

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-10-cyfrin-casimir-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md)_

---

**Description:** A validator can reshare an operator if its either in `PENDING` or `ACTIVE` status. When resharing is executed for a validtor in `PENDING` state , the existing operators are removed from the SSV cluster -> however,  no such operators are registered in the first place. This is because SSV registration does not happen when `depositStake` is called.

```solidity
 function reshareValidator(
        uint32 validatorId,
        uint64[] memory operatorIds,
        uint64 newOperatorId,
        uint64 oldOperatorId,
        bytes memory shares,
        ISSVClusters.Cluster memory cluster,
        ISSVClusters.Cluster memory oldCluster,
        uint256 feeAmount,
        uint256 minTokenAmount,
        bool processed
    ) external {
        onlyReporter();

        Validator storage validator = validators[validatorId];
        if (validator.status != ValidatorStatus.ACTIVE && validator.status != ValidatorStatus.PENDING) {
            revert ValidatorNotActive();
        }

       // ... code

        uint256 ssvAmount = retrieveFees(feeAmount, minTokenAmount, address(ssvToken), processed);
        ssvToken.approve(address(ssvClusters), ssvAmount);
>        ssvClusters.removeValidator(validator.publicKey, validator.operatorIds, oldCluster); //@audit validtor key is not registered when the validator is in pending state
       ssvClusters.registerValidator(validator.publicKey, operatorIds, shares, ssvAmount, cluster); //@audit new operators registered

        validator.operatorIds = operatorIds;
        validator.reshares++;

        registry.removeOperatorValidator(oldOperatorId, validatorId, 0);
        registry.addOperatorValidator(newOperatorId, validatorId);

        emit ValidatorReshared(validatorId);
    }
```



`SSVCluster::removeValidator` reverts when it can't find a validator data to remove.

```solidity
    function removeValidator(
        bytes calldata publicKey,
        uint64[] memory operatorIds,
        Cluster memory cluster
    ) external override {
        StorageData storage s = SSVStorage.load();

        bytes32 hashedCluster = cluster.validateHashedCluster(msg.sender, operatorIds, s);
        bytes32 hashedOperatorIds = ValidatorLib.hashOperatorIds(operatorIds);

        bytes32 hashedValidator = keccak256(abi.encodePacked(publicKey, msg.sender));
        bytes32 validatorData = s.validatorPKs[hashedValidator];

        if (validatorData == bytes32(0)) {
>            revert ISSVNetworkCore.ValidatorDoesNotExist(); //@audit reverts when no key exists
        }

        if (!ValidatorLib.validateCorrectState(validatorData, hashedOperatorIds))
            revert ISSVNetworkCore.IncorrectValidatorStateWithData(publicKey);

        delete s.validatorPKs[hashedValidator];

        if (cluster.active) {
            StorageProtocol storage sp = SSVStorageProtocol.load();
            (uint64 clusterIndex, ) = OperatorLib.updateClusterOperators(operatorIds, false, false, 1, s, sp);

            cluster.updateClusterData(clusterIndex, sp.currentNetworkFeeIndex());

            sp.updateDAO(false, 1);
        }

        --cluster.validatorCount;

        s.clusters[hashedCluster] = cluster.hashClusterData();

        emit ValidatorRemoved(msg.sender, operatorIds, publicKey, cluster);
    }
```

**Impact:** An operator requesting a deactivation after initial deposit cannot be reshared.

**Recommended Mitigation:** Consider either of the 2 options:
- If resharing at PENDING stage needs to be supported, then register operators in `depositStake`
- If resharing at PENDING stage should not be supported, disallow resharing for validators in `Status.PENDING` in the `reshareValidator`

**Casimir:**
Fixed in [cd03c74](https://github.com/casimirlabs/casimir-contracts/commit/cd03c740c457264e578945bb2a8cc8bcf2c875f8)

**Cyfrin:** Verified.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-10-cyfrin-benqi-governance-v2-0-0-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-11-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-10-cyfrin-benqi-governance-v2-0
title: Maximum number of Aragon DAO actions is not checked within the `DistributorManager`
vuln_class: []
---

# Maximum number of Aragon DAO actions is not checked within the `DistributorManager`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-10-cyfrin-benqi-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md)_

---

**Description:** The `DistributionManager` generates actions for reward distribution but does not currently validate against the DAO's `MAX_ACTIONS` limit before calling `dao.execute()`. The Aragon DAO has a hard limit of 256 actions per execution:

```solidity
// lib/conditions/lib/osx/packages/contracts/src/core/dao/DAO.sol
uint256 internal constant MAX_ACTIONS = 256;

function execute(
        bytes32 _callId,
        Action[] calldata _actions,
        uint256 _allowFailureMap
    )
        external
        override
        nonReentrant
        auth(EXECUTE_PERMISSION_ID)
        returns (bytes[] memory execResults, uint256 failureMap)
    {
        // Check that the action array length is within bounds.
@>      if (_actions.length > MAX_ACTIONS) {
            revert TooManyActions();
        }
        ...
}
```

But `DistributionManager` calculates the action count without validating against this limit:

```
 function distribute() external auth(DISTRIBUTOR_ROLE) {
    ...
    IExecutor(address(dao())).execute({
        _callId: _generateCallId(),
        _actions: actions, // @audit - no length validation
        _allowFailureMap: 0
    });
    emit RewardsDistributed(currentEpochId);
}
```

Note that there are similarly no limitations on the number of gauges and controllers that are allowed in the system.

**Impact:** Reaching the action limit could lead to temporary DoS.

**Recommended Mitigation:** While it is unlikely that this scenario will occur, consider explicitly limiting the number of actions in the `DistributionManager`.

**BENQI:** Acknowledged.

**Cyfrin:** Acknowledged.

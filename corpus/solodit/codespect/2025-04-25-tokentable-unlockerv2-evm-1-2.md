---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-25-tokentable-unlockerv2-evm-1-2
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-04-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-25-TokenTable-UnlockerV2-EVM.md
tags:
- firm:codespect
- report:2025-04-25-tokentable-unlockerv2-evm
title: '[L-03] Unauthorized claims allowed when externalDelegateRegistry is not configured'
vuln_class: []
---

# [L-03] Unauthorized claims allowed when externalDelegateRegistry is not configured

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-25-TokenTable-UnlockerV2-EVM.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-25-TokenTable-UnlockerV2-EVM.md)_

---

**Files:** [TokenTableUnlockerV2.sol](https://github.com/EthSign/tokentable-v2-evm/blob/e27192f627ea849f88e8a4b68382c5ac8808e3a5/contracts/core/TokenTableUnlockerV2.sol#L153-L154)

**Description:**

The `TokenTableUnlockerV2` contract allows designated users to claim tokens on behalf of others via the `delegateClaim(...)` function. A caller can perform this action only if they are:

1. Included in the internal `claimingDelegates` set, or;
2. Authorised via an external delegate registry (if one is configured);

Only the contract owner can manage the `claimingDelegates` list. If an external registry is configured, it will be used to verify whether the `msg.sender` has permission to make a claim on behalf of the original token owner.

```solidity
function delegateClaim(uint256[] calldata actualIds, ...)
    ...
{
    TokenTableUnlockerV2Storage storage $ = _getTokenTableUnlockerV2Storage();
    bool callerIsClaimingDelegate = $.claimingDelegates.contains(_msgSender());
    for (uint256 i = 0; i < actualIds.length; i++) {
        if (
            // @audit statement incorrect
            !callerIsClaimingDelegate && $.currentChainSupportsExternalDelegateRegistry
                && !externalDelegateRegistry.checkDelegateForContract(
                    _msgSender(), $.futureToken.ownerOf(actualIds[i]), address(this), this.delegateClaim.selector
                )
        ) {
            revert NotPermissioned();
        }
        _claim(actualIds[i], address(0), batchId);
    }
    _callHook(_msgData());
}
```

The logic inside the `if` condition is flawed. The intention is to *revert* if the caller is **not** a claiming delegate **and not** authorised via the registry. However, due to the current structure, this is not correctly enforced when the external registry is **not configured**.

Example case where the registry is not configured:

- `callerIsClaimingDelegate = false;`
- `currentChainSupportsExternalDelegateRegistry = false;`

The condition evaluates to:

```text
!false && false => true && false => false
```

This incorrectly allows execution to continue, letting unauthorised users claim on behalf of others if the registry is not enabled.

**Impact:** This breaks the core invariant of the `delegateClaim` logic. Unauthorised users can claim tokens for others when the external registry is not set, potentially compromising any contracts that integrate with `TokenTableUnlockerV2`.

**Recommendation:** Refactor the conditional logic to clearly enforce that only a permitted claiming delegate or a registry-authorized user can claim on behalf of others.

**Status:** Fixed

**Update from TokenTable:** [661c34353311d27ad03f35f9066a7a772d5be6d0](https://github.com/EthSign/tokentable-v2-evm/pull/11/commits/661c34353311d27ad03f35f9066a7a772d5be6d0)

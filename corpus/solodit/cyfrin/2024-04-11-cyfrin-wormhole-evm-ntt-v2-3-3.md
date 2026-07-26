---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-3-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-04-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md
tags:
- firm:cyfrin
- report:2024-04-11-cyfrin-wormhole-evm-ntt-v2
title: Unused `PausableUpgradeable::CannotRenounceWhilePaused` error should be removed
vuln_class: []
---

# Unused `PausableUpgradeable::CannotRenounceWhilePaused` error should be removed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-11-cyfrin-wormhole-evm-ntt-v2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md)_

---

[`PausableUpgradeable::CannotRenounceWhilePaused`](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/libraries/PausableUpgradeable.sol#L50-L53) is a custom error defined as follows:
```solidity
/**
 * @dev Cannot renounce the pauser capability when the contract is in the `PAUSED` state
 */
error CannotRenounceWhilePaused(address account);
```
The above error and inline comments imply that the pauser capability cannot be transferred when a contract is in a `PAUSED` state. However, no such check is performed in `PausableOwnable::transferPauserCapability`:

```solidity
/**
 * @dev Transfers the ability to pause to a new account (`newPauser`).
 */
function transferPauserCapability(address newPauser) public virtual onlyOwnerOrPauser {
    PauserStorage storage $ = _getPauserStorage();
    address oldPauser = $._pauser;
    $._pauser = newPauser;
    emit PauserTransferred(oldPauser, newPauser);
}
```

Given that it is understood this is not an error of omission, where stated functionality is not implemented in the function, but rather an unused custom error that is not intended to be used, it is recommended that the definition be removed.

**Wormhole Foundation:** Fixed in [PR \#244](https://github.com/wormhole-foundation/example-native-token-transfers/pull/244).

**Cyfrin:** Verified. The unused error has been removed.

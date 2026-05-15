---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-4-7
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: Emergency mode doesn't save from malicious upgrade of StakeManager.sol
vuln_class: []
---

# Emergency mode doesn't save from malicious upgrade of StakeManager.sol

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** Documentation describes that one of scenarios when emergency mode will be used is malicious upgrade of `StakingManager.sol`
https://github.com/status-im/status-network-monorepo/blob/develop/status-network-contracts/docs/staking-reward-distributor/emergency-mode.md#when-emergency-mode-is-used
>If the StakeManager is upgraded to a malicious or broken implementation, guardians can enable emergency mode to allow users to exit before interacting with the compromised contract.

It's implemented as following:
```solidity
    function emergencyExit(address _destination) external onlyOwner validDestination(_destination) {
        depositedBalance = 0;
        try stakeManager.emergencyModeEnabled() returns (bool enabled) {
            if (!enabled) {
                revert StakeVault__NotAllowedToExit();
            }
            bool success = STAKING_TOKEN.transfer(_destination, STAKING_TOKEN.balanceOf(address(this)));
            if (!success) {
                revert StakeVault__FailedToExit();
            }
        } catch {
            bool success = STAKING_TOKEN.transfer(_destination, STAKING_TOKEN.balanceOf(address(this)));
            if (!success) {
                revert StakeVault__FailedToExit();
            }
        }
    }
```
However if attacker can upgrade `StakeManager.sol`, then he can for example remove function `emergencyModeEnabled` so that try-catch doesn't work, or make `emergencyModeEnabled` return `false`. Yes there is no ability to steal staked tokens, but he still can brick them.

**Impact:** In case of malicious upgrade of `StakeManager.sol`, attacker can block users from withdrawing staked tokens.

**Recommended Mitigation:** It's not immediately obvious how to save tokens from bricking in case of `StakeManager.sol` owner compromise in current design. At least update docs to document it.

**StatusL2:** Fixed in [7401475](https://github.com/status-im/status-network-monorepo/commit/7401475b4918319e627eb3ba7df24a498f8d063f).

**Cyfrin:** Verified.

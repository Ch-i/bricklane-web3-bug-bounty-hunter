---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-23-cyfrin-strata-shares-cooldown-v2-0-2-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-01-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-23-cyfrin-strata-shares-cooldown-v2-0
title: Unreachable code on `SharesCooldown::requestRedeem`
vuln_class: []
---

# Unreachable code on `SharesCooldown::requestRedeem`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md)_

---

**Description:** `SharesCooldown::requestRedeem` has a conditional to handle the case when `cooldownSeconds` is received as 0 (instant redemption), but, this function is only called when `cooldownSeconds > 0`.
- `StrataCDO::calculateExitMode` assigns the `exitMode` as `SharesLock` only when `exit.sharesLock > 0`, and, `Tranche::_withdraw` calls `CDO::cooldownShares` only when `exitMode` is `sharesLock`.
```solidity
    function calculateExitMode (address tranche, address owner) external view returns (TExitMode mode, uint256 fee, uint32 cooldownSeconds) {
        if (address(sharesCooldown) != address(0)) {
            ...
            if (exit.sharesLock > 0) {
//@audit => exitMode is set as SharesLock only when a cooldown will be applied
@>              return (TExitMode.SharesLock, fee, exit.sharesLock);
            }
        }
        ...
    }

    function _withdraw(
        ...
    ) internal virtual {
        ...

//@audit => CDO.cooldownshares gets called only when exitMode is set as SharesLock
        if (exitMode == IStrataCDO.TExitMode.SharesLock) {
            ...
            cdo.cooldownShares(address(this), sharesGross, owner, receiver, exitFee, cooldownSec);
            return;
        }

        ...
        cdo.withdraw(address(this), token, tokenAssets, baseAssets, owner, receiver);
        ...
    }

```

**Recommended Mitigation:** Consider [removing the case when `cooldownSeconds` is 0,](https://github.com/Strata-Money/contracts-tranches/blob/219880e7a6d43a88d91b1ff3c1f94cea1082bbc9/contracts/tranches/base/cooldown/SharesCooldown.sol#L60-L64) as the execution flow won't call `CooldownShares.requestRedeem` when there is no cooldown.

**Strata:** Acknowledged. In the current flow, the check and instant redemption path is indeed unreachable; however, we prefer to keep it for consistency with ERC20Cooldown, and in case we later introduce additional flows from other strategies that do not include this initial check.

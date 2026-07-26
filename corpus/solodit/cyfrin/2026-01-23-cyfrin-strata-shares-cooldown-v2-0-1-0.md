---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-23-cyfrin-strata-shares-cooldown-v2-0-1-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-01-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-23-cyfrin-strata-shares-cooldown-v2-0
title: Invalid validateRedemptionParams check
vuln_class: []
---

# Invalid validateRedemptionParams check

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md)_

---

**Description:** The `withdraw` and `redeem` functions were designed to provide UX-level slippage protection by requiring user-supplied exit parameters to match the protocol-calculated exit mode. If conditions change, the transaction is expected to revert, as stated by the protocol.

However, `validateRedemptionParams` currently returns instead of reverting when user parameters do not match system parameters. This completely pass any slippage protection and breaking the UX guarantee described by the team.

```solidity
function validateRedemptionParams(TRedemptionParams memory params, IStrataCDO.TExitMode exitMode, uint256 exitFee, uint32 cooldownSec) internal pure {
        if (params.exitMode == IStrataCDO.TExitMode.Dynamic) {
            return;
        }
        if (params.exitMode != exitMode || params.exitFee != exitFee || params.cooldownSeconds != cooldownSec) {
            return;
        }
        revert RedemptionParamsMismatch(params, TRedemptionParams({
            exitMode: exitMode,
            exitFee: exitFee,
            cooldownSeconds: cooldownSec
        }));
    }
```

**Recommended Mitigation:** The `validateRedemtionParams` function should revert instead of return if at least one of the parameters does not match. Also, revert at the end of the function should be replaced with return.

**Strata:** Fixed in commit **652a5c1**

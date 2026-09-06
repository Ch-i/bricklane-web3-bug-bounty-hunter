---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-23-cyfrin-strata-shares-cooldown-v2-0-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-01-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-23-cyfrin-strata-shares-cooldown-v2-0
title: Finalizing withdrawal requests on the `SharesCooldown` contract allows for
  third-parties to override user’s chosen output token
vuln_class: []
---

# Finalizing withdrawal requests on the `SharesCooldown` contract allows for third-parties to override user’s chosen output token

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md)_

---

**Description:** During `Tranche::withdraw/redeem`, the user can select the desired output token. However, when the exit mode is `SharesLock`, the final token received by the user is no longer under the user's control.

- SharesCooldown finalization is permissionless, allowing any caller to choose the output token at finalization time. This enables third parties to finalize the user’s claim using a different token than the one the user originally intended.
```solidity
    function finalize(ITranche vault, address token, address user) external returns (uint256 claimed) {
        return finalize(vault, token, user, block.timestamp);
    }
    function finalize(ITranche vault, address token, address user, uint256 at) public returns (uint256 claimed) {
        claimed = extractClaimableInner(address(vault), user, at);
        vault.redeem(token, claimed, user, address(this));
        emit Finalized(vault, user, claimed);
        return claimed;
    }
```

This is problematic because the final time it takes for the withdrawers to receive the assets can be extended beyond what they are comfortable waiting for. For example, consider the scenario where a user selects `sUSDe` as the `outputToken`. Here is what would happen when finalizing such a withdrawal request on the `SharesCooldown` contract:
1. If finalization selects `sUSDe`, then the `cooldown` period was the only time the user had to wait to receive his assets.
2. If finalization selects `USDe`, then, on top of the `cooldown` period, the user will have to wait for the `unstaking` period on the `sUSDe` contract, and, only until the `unstaking` period is over, the user will be able to get their assets back finally.


**Recommended Mitigation:** Persist the user’s chosen output token when creating the cooldown request and enforce it during a permissionless finalization.

**Strata:** Fixed in commit [0354983](https://github.com/Strata-Money/contracts-tranches/commit/03549831cf5912b15d9a0eac2bdcfae7e1c395d8).

**Cyfrin:** Verified. Permissionless finalizations can't override the user's original choice; only the user can override the redeemable token via a permissioned function. Now it is possible to finalize only requests for a specific token at a time.

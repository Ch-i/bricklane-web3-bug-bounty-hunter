---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-12-cyfrin-bebop-router-v2-0-2-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-06-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-12-cyfrin-bebop-router-v2-0
title: '`BebopRouter::_approveHooks` never resets hook ERC20 allowance, leaving a
  standing approval to routerSigner-authorized hook targets'
vuln_class: []
---

# `BebopRouter::_approveHooks` never resets hook ERC20 allowance, leaving a standing approval to routerSigner-authorized hook targets

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-12-cyfrin-bebop-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md)_

---

**Description:** `_approveHooks` calls `safeApproveWithRetry(hook.targetContract, amount)` for each hook that has `needsApproval` set:

```solidity
// contracts/BebopRouter.sol:322-326
function _approveHooks(Hook[] calldata hooks, bool postHookPhase, address token, uint256 amount) internal {
    for (uint256 i; i < hooks.length; ++i) {
        if (HookLib.isPostHook(hooks[i]) == postHookPhase && HookLib.isNeedsApproval(hooks[i])) {
            IERC20(token).safeApproveWithRetry(hooks[i].targetContract, amount);
        }
    }
}
```

The allowance is set before the hook phase executes and is never reset to zero afterward. For the pre-hook phase, each `needsApproval` hook receives an allowance for `ctx.calc.newFromAmount` of `order.fromToken`. For the post-hook phase, each `needsApproval` hook receives an allowance for the router's full current `order.pmmToToken` balance:

```solidity
// contracts/BebopRouter.sol:289
_approveHooks(hooks, true, order.pmmToToken, IERC20(order.pmmToToken).balanceOf(address(this)));
```

Hooks with `makerAddress == address(0)` require no maker signature because `_validateHookSignatures` skips them. They are still bound into the routerSigner-signed order through `hooksHash`, so arbitrary third parties cannot inject these approvals. However, once the routerSigner authorizes a hook target with `needsApproval = true`, any unused allowance to that target persists after the swap.

This is most visible when a hook target consumes less than the approved amount, when a hook is a no-op, or when multiple `needsApproval` hooks exist in the same phase: `_approveHooks` grants every matching hook the full allowance before execution, while only one hook may actually consume the balance.

**Files:**

- `contracts/BebopRouter.sol` - `BebopRouter::_approveHooks` (lines 322-328)
- `contracts/BebopRouter.sol` - `BebopRouter::_executeSwapCore` (line 289)

**Impact:** A standing ERC20 allowance granted to a hook target persists indefinitely. If the router later holds a persistent balance of that same token - for example from a donation, stranded input/output, or accumulated dust - the approved hook target can call `transferFrom` directly and drain up to the leftover allowance without another router call.

This is not a permissionless exploit: the original approval requires a routerSigner-signed order naming that hook target, and the hook system is an intended trusted extension point. The issue is a blast-radius and cleanup gap. A hook that was authorized for one swap keeps spending power over future residual balances even after that swap completes.

**Recommended Mitigation:** Reset each hook target's allowance to zero immediately after the relevant hook phase executes. Approve only for the duration of the hook call, then clear the allowance regardless of whether the hook consumed the full amount. Also consider replacing the phase-wide full-balance approval with per-hook declared consumption limits, or require hook targets to be allowlisted.

**Bebop:** Fixed in commit [9db95bc](https://github.com/bebop-dex/bebop-rfqa/commit/9db95bc2b423d9317c149e90a70ae51565e26367).

**Cyfrin:**
Verified.

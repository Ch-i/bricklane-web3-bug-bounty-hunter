---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-1-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-07-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-17-cyfrin-octodefi-v2-0
title: Volume-based fee can be bypassed with a wrapper contract
vuln_class: []
---

# Volume-based fee can be bypassed with a wrapper contract

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-17-cyfrin-octodefi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md)_

---

**Description:** `_executeAction()` levies a percentage fee only when `FeeController.getTokenForAction()` can map the `(target, selector)` pair to a tracked token. If the mapping is absent it falls back to `minFeeInUSD`.
An attacker can therefore wrap any high-value call inside a helper contract that the `FeeController` does not know about.
*Example – Aave deposit:*
```text
User → StrategyBuilder → AAVEHandler.supplyFor(100 000 USDC) → Aave Pool.supply()
```
`AAVEHandler` receives the user’s 100 000 USDC, approves the Aave pool, and supplies on the user’s behalf, returning aUSDC. Because `(AAVEHandler, supplyFor)` is not registered, `getTokenForAction()` returns `(address(0), false)`, so the strategy pays only the minimum fee instead of ~1 000 USDC (1 %). The same trick works for withdrawals, swaps, or any volume-based selector.

```solidity
function _executeAction(address _wallet, Action memory _action) internal returns (uint256 feeInUSD) {
    (address tokenToTrack, bool exist) =
        feeController.getTokenForAction(_action.target, _action.selector, _action.parameter);
    // If the volume token exist track the volume before and after the execution, else get the min fee

    uint256 preExecBalance = exist ? IERC20(tokenToTrack).balanceOf(_wallet) : 0;

    _execute(_wallet, _action);

    IFeeController.FeeType feeType = feeController.functionFeeConfig(_action.selector).feeType;

    if (exist) {
        uint256 postExecBalance = IERC20(tokenToTrack).balanceOf(_wallet);
        uint256 volume = feeType == IFeeController.FeeType.Deposit
            ? preExecBalance - postExecBalance
            : postExecBalance - preExecBalance;

        feeInUSD = feeController.calculateFee(tokenToTrack, _action.selector, volume);
    } else {
        feeInUSD = feeController.minFeeInUSD(feeType);
    }

    emit ActionExecuted(_wallet, _action);
}
```
**Impact:** Large transactions can be executed while paying the protocol’s minimum flat fee, severely reducing or eliminating expected revenue for executors.

**Recommended Mitigation:** Because this stems from design choices rather than a simple coding bug, solving it on-chain is non-trivial. It is to document the behavior and discuss any design adjustment that can remediate its risk.

**OctoDeFi:** Fixed in PR [\#25](https://github.com/octodefi/strategy-builder-plugin/pull/25).

**Cyfrin:** Verified. The `ActionRegistry` contract has been added to validate action contracts allowed to be integrated into `StrategyBuilderPlugin`.

\clearpage

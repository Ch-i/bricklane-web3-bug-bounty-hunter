---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-parallel3-1-v2-0-2-5
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-parallel3-1-v2-0
title: '`SettersGovernor::setWhitelistStatus` allows values other than 0 and 1 potentially
  leading to DOS'
vuln_class: []
---

# `SettersGovernor::setWhitelistStatus` allows values other than 0 and 1 potentially leading to DOS

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-parallel3.1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md)_

---

**Description:** Until Parallel protocol added `setWhitelistStatus` the only way to change the `whitelistStatus` in the `isWhitelistedForType` mapping was to use `SettersGuardian::toggleWhitelist`.

It is clear from this code that the only "reachable" values values are `0` and `1`, since the value starts initialised at `0` and `1 - 0 == 1` and `1 - 1 == 0`.

However `setWhitelistStatus` actually allows values in the range 2 - 255. If a governor were to call it with any of these values this leads to a DOS on any function that indirectly calls `LibWhitelist::checkWhitelist`

The root causes are marked lines in `LibSetters::setWhitelistStatus`.

```solidity
    if (whitelistStatus == 1) {
    ...
    } else {
        // If whitelist is revoked, clear the whitelist data
@>      collatInfo.whitelistData = "";
    }
@>  collatInfo.onlyWhitelisted = whitelistStatus;
```

If called with `whitelistStatus > 1` then `collatInfo.whitelistData` is set to empty bytes and `collatInfo.onlyWhitelisted > 1` after execution.

If we later call a function that indirectly calls `_redeem` or `_swap` then the following following statement is executed

```solidity
if (collatInfo.onlyWhitelisted > 0 && !LibWhitelist.checkWhitelist(collatInfo.whitelistData, to)) {
    revert NotWhitelisted();
}
```

Since `collatInfo.onlyWhitelisted > 1` we now call `LibWhitelist.checkWhitelist`

Unfortunately this will revert on the first line in the `abi.decode`

```solidity
function checkWhitelist(bytes memory whitelistData, address sender) internal returns (bool) {
@>  (WhitelistType whitelistType, bytes memory data) = abi.decode(whitelistData, (WhitelistType, bytes));
```
**Impact:** The protocol will be DOSed for any swaps or redeems. The impact is low since governance can just call it again with `whitelistStatus == 0` and the chance of making this mistake in the first place is low.

However, if `SettersGovernor::setAccessManager` were called with an `AccessManager` that were configured to impose delays the DOS could be more serious. See [LibDiamond::checkCanCall](https://github.com/parallel-protocol/parallel-core/blob/main/Parallel-Parallelizer/contracts/parallelizer/libraries/LibDiamond.sol#L31-L46) and the `delay > 0` branch.

**Proof of Concept:** In `tests/units/parallel-protocolWhitelistStatusDos.t.sol` we have
- [test_parallel-protocol_WhitelistStatusTwo_DOSesBurnSwapExactInput](https://github.com/parallel-protocol/parallel-core/blob/audit/100proof/Parallel-Parallelizer/tests/units/parallel-protocolWhitelistStatusDos.t.sol#L20-L46) which tests
- [test_parallel-protocol_WhitelistStatusTwo_DOS_RequiresDelayToUndo](https://github.com/parallel-protocol/parallel-core/blob/audit/100proof/Parallel-Parallelizer/tests/units/parallel-protocolWhitelistStatusDos.t.sol#L48C12-L104) which shows delays can make the DOS more serious. It lasts as long as the `delay` set for the `GOVERNOR_ROLE`.
```solidity
// SPDX-License-Identifier: BUSL-1.1

pragma solidity 0.8.28;

import "contracts/parallelizer/Storage.sol";
import "contracts/utils/Constants.sol";
import { ISettersGovernor } from "contracts/interfaces/ISetters.sol";
import { MockChainlinkOracle } from "tests/mock/MockChainlinkOracle.sol";
import { Fixture } from "../Fixture.sol";

contract CyfrinWhitelistStatusDos is Fixture {
  function _refreshOracles() internal {
    // The oracle configs use a 1-hour stale period. We warp a full day to model the delay,
    // so we must refresh all collateral oracles or burns will revert with InvalidChainlinkRate.
    MockChainlinkOracle(address(oracleA)).setLatestAnswer(int256(BASE_8));
    MockChainlinkOracle(address(oracleB)).setLatestAnswer(int256(BASE_8));
    MockChainlinkOracle(address(oracleY)).setLatestAnswer(int256(BASE_8));
  }

  function test_cyfrin_WhitelistStatusTwo_DOSesBurnSwapExactInput() public {
    uint256 amountIn = 100 * BASE_6;

    vm.startPrank(alice);
    deal(address(eurA), alice, amountIn);
    eurA.approve(address(parallelizer), type(uint256).max);
    uint256 minted = parallelizer.swapExactInput(
      amountIn, 0, address(eurA), address(tokenP), alice, block.timestamp + 1
    );
    tokenP.approve(address(parallelizer), type(uint256).max);
    vm.stopPrank();

    uint256 snap = vm.snapshotState();
    vm.startPrank(alice);
    parallelizer.swapExactInput(minted, 0, address(tokenP), address(eurA), alice, block.timestamp + 1);
    vm.stopPrank();
    vm.revertToState(snap);

    bytes memory whitelistData = abi.encode(WhitelistType.BACKED, bytes(""));
    hoax(governor);
    parallelizer.setWhitelistStatus(address(eurA), 2, whitelistData);

    vm.startPrank(alice);
    vm.expectRevert();
    parallelizer.swapExactInput(minted, 0, address(tokenP), address(eurA), alice, type(uint256).max);
    vm.stopPrank();
  }

  function test_cyfrin_WhitelistStatusTwo_DOS_RequiresDelayToUndo() public {
    uint256 amountIn = 100 * BASE_6;

    vm.startPrank(alice);
    deal(address(eurA), alice, amountIn);
    eurA.approve(address(parallelizer), type(uint256).max);
    uint256 minted = parallelizer.swapExactInput(
      amountIn, 0, address(eurA), address(tokenP), alice, block.timestamp + 1
    );
    tokenP.approve(address(parallelizer), type(uint256).max);
    vm.stopPrank();

    // Set a 1-day delay for governor actions.
    vm.startPrank(governor);
    accessManager.grantRole(GOVERNOR_ROLE, governor, 86400);
    vm.stopPrank();
    (,, uint32 pendingDelay, uint48 effect) = accessManager.getAccess(GOVERNOR_ROLE, governor);
    if (pendingDelay > 0 && effect > block.timestamp) {
      vm.warp(effect);
    }
    (, uint32 currentDelay,,) = accessManager.getAccess(GOVERNOR_ROLE, governor);

    bytes memory whitelistData = abi.encode(WhitelistType.BACKED, bytes(""));
    bytes memory setToTwo =
      abi.encodeCall(ISettersGovernor.setWhitelistStatus, (address(eurA), uint8(2), whitelistData));

    vm.startPrank(governor);
    accessManager.schedule(address(parallelizer), setToTwo, 0);
    // Must wait the delay before executing the scheduled op.
    vm.warp(block.timestamp + currentDelay);
    accessManager.execute(address(parallelizer), setToTwo);
    vm.stopPrank();

    _refreshOracles();
    vm.startPrank(alice);
    vm.expectRevert();
    parallelizer.swapExactInput(minted, 0, address(tokenP), address(eurA), alice, type(uint256).max);
    vm.stopPrank();

    bytes memory clearWhitelist =
      abi.encodeCall(ISettersGovernor.setWhitelistStatus, (address(eurA), uint8(0), bytes("")));

    vm.startPrank(governor);
    accessManager.schedule(address(parallelizer), clearWhitelist, 0);
    // Cannot execute immediately; must wait the delay.
    vm.expectRevert();
    accessManager.execute(address(parallelizer), clearWhitelist);
    vm.warp(block.timestamp + currentDelay);
    accessManager.execute(address(parallelizer), clearWhitelist);
    vm.stopPrank();

    _refreshOracles();
    vm.startPrank(alice);
    parallelizer.swapExactInput(minted, 0, address(tokenP), address(eurA), alice, type(uint256).max);
    vm.stopPrank();
  }
}
```

**Recommended Mitigation:** Add a check at the beginning of `LibSetters::setWhitelistStatus`

```diff
  function setWhitelistStatus(address collateral, uint8 whitelistStatus, bytes memory whitelistData) internal {
+   if (whitelistStatus > 1) revert InvalidWhitelistStatus();
    Collateral storage collatInfo = s.transmuterStorage().collaterals[collateral];
    if (collatInfo.decimals == 0) revert NotCollateral();
```

**Parallel:** Fixed in commit [3010a17](https://github.com/parallel-protocol/parallel-parallelizer/commit/3010a17b3780a508e27d4a8200e9c73a61addf99#diff-41e3c405851499899c192341a0bd4b5587ba64730ba738b5db5ebba0a08de5c2).

**Cyfrin:** Verified. Implemented recommended mitigation.

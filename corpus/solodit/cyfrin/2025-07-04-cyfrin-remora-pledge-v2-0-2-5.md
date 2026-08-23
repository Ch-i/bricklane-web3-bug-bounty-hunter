---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-2-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Zero token transfers record receiving user as a holder in `DividendManager::HolderStatus`
  even if they have zero token balance
vuln_class: []
---

# Zero token transfers record receiving user as a holder in `DividendManager::HolderStatus` even if they have zero token balance

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** Zero token transfers record receiving user as a holder in `DividendManager::HolderStatus` even if they have zero token balance.

**Proof of Concept:** First add these two functions in `DividendManager`:
```solidity
function getCurrentPayoutIndex() view external returns(uint8 currentPayoutIndex) {
    currentPayoutIndex = _getHolderManagementStorage()._currentPayoutIndex;
}

function getHolderStatus(address holder) view external returns(HolderStatus memory status) {
    status = _getHolderManagementStorage()._holderStatus[holder];
}
```

Then the PoC:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {RemoraToken, DividendManager} from "../../../contracts/RWAToken/RemoraToken.sol";
import {Stablecoin} from "../../../contracts/ForTestingOnly/Stablecoin.sol";
import {AccessManager} from "../../../contracts/AccessManager.sol";
import {Allowlist} from "../../../contracts/Allowlist.sol";

import {UnitTestBase} from "../UnitTestBase.sol";

import {ERC1967Proxy} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";

contract RemoraTokenTest is UnitTestBase {
    // contract being tested
    RemoraToken remoraTokenProxy;
    RemoraToken remoraTokenImpl;

    // required support contracts & variables
    Stablecoin internal stableCoin;
    AccessManager internal accessMgrProxy;
    AccessManager internal accessMgrImpl;
    Allowlist internal allowListProxy;
    Allowlist internal allowListImpl;
    address internal withdrawalWallet;
    uint32 internal constant DEFAULT_PAYOUT_FEE = 100_000; // 10%

    function setUp() public override {
        // test harness setup
        UnitTestBase.setUp();

        // support contracts / variables setup
        stableCoin = new Stablecoin("USDC", "USDC", type(uint256).max/1e6, 6);
        assertEq(stableCoin.balanceOf(address(this)), type(uint256).max/1e6*1e6);

        // contract being tested setup
        accessMgrImpl = new AccessManager();
        ERC1967Proxy proxy1 = new ERC1967Proxy(address(accessMgrImpl), "");
        accessMgrProxy = AccessManager(address(proxy1));
        accessMgrProxy.initialize(address(this));

        allowListImpl = new Allowlist();
        ERC1967Proxy proxy2 = new ERC1967Proxy(address(allowListImpl), "");
        allowListProxy = Allowlist(address(proxy2));
        allowListProxy.initialize(address(accessMgrProxy), address(this));

        withdrawalWallet = makeAddr("WITHDRAWAL_WALLET");

        // contract being tested setup
        remoraTokenImpl = new RemoraToken();
        ERC1967Proxy proxy3 = new ERC1967Proxy(address(remoraTokenImpl), "");
        remoraTokenProxy = RemoraToken(address(proxy3));
        remoraTokenProxy.initialize(
            address(this), // tokenOwner
            address(accessMgrProxy), // initialAuthority
            address(stableCoin),
            withdrawalWallet,
            address(allowListProxy),
            "REMORA",
            "REMORA",
            0
        );

        assertEq(remoraTokenProxy.authority(), address(accessMgrProxy));
    }

    function test_transferZeroTokens_RegistersHolderWithDividendManager() external {
        address user1 = users[0];
        address user2 = users[1];

        uint256 user1RemoraTokens = 1;

        // whitelist both users
        remoraTokenProxy.addToWhitelist(user1);
        assertTrue(remoraTokenProxy.isWhitelisted(user1));
        remoraTokenProxy.addToWhitelist(user2);
        assertTrue(remoraTokenProxy.isWhitelisted(user2));

        // mint user1 their tokens
        remoraTokenProxy.mint(user1, user1RemoraTokens);
        assertEq(remoraTokenProxy.balanceOf(user1), user1RemoraTokens);

        // allowlist both users
        allowListProxy.allowUser(user1, true, true, false);
        assertTrue(allowListProxy.allowed(user1));
        allowListProxy.allowUser(user2, true, true, false);
        assertTrue(allowListProxy.allowed(user2));
        assertTrue(allowListProxy.exchangeAllowed(user1, user2));

        // user1 transfers zero tokens to user2
        vm.prank(user1);
        remoraTokenProxy.transfer(user2, 0);

        // fetch user2's HoldStatus from DividendManager
        DividendManager.HolderStatus memory user2Status = remoraTokenProxy.getHolderStatus(user2);

        // user2 is listed as a holder even though they have no tokens!
        assertEq(user2Status.isHolder, true);
        assertEq(remoraTokenProxy.balanceOf(user2), 0);
    }
}
```

**Recommended Mitigation:** Either revert on zero token transfers inside `RemoraToken::_update` or change `DividendManager::_updateHolders` to not set `to` as a holder if their balance is zero.

**Remora:** Fixed in commit [0a2dea2](https://github.com/remora-projects/remora-smart-contracts/commit/0a2dea21b8dec5fa63dd2402b987b4f77c3e60b1).

**Cyfrin:** Verified.

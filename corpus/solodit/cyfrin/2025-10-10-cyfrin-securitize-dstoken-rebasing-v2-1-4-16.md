---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-4-16
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Not possible to send native via the `TransactionRelayer` to the target contract
  when executing `executeByInvestorWithBlockLimit`
vuln_class: []
---

# Not possible to send native via the `TransactionRelayer` to the target contract when executing `executeByInvestorWithBlockLimit`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** `TransactionRelayer::executeByInvestorWithBlockLimit` makes an external call to a `destination` address, one of the input parameters of this function is `value`, which is encoded in `params[0]`, and this parameter is used to specify the amount of native balance that will be transferred to the `destination` address on the external call made in `doExecuteByInvestor`.

The problem is that the `TransactionRelayer::executeByInvestorWithBlockLimit` is not payable, which means that native can't be sent as part of the txn. Also, `TransactionRelayer` reverts when attempting to fund it by transferring native from one account to another.
```solidity
    function doExecuteByInvestor(
        ...
        uint256[] memory params
    ) private {
       ...
        bool success = false;
        uint256 value = params[0];
        uint256 gasLimit = params[1];
        assembly {
            success := call(
            gasLimit,
            destination,
//@audit => Amount of native to transfer on the external call
            value,
            add(data, 0x20),
            mload(data),
            0,
            0
            )
        }
        require(success, "transaction was not executed");
    }
```

**Impact:** Signatures including native balance to be sent to the target contract will revert.

**Proof of Concept:** Add the next foundry PoC to the test suite.
```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.22;

import "forge-std/Test.sol";
import "../contracts/utils/TransactionRelayer.sol";
import {ERC1967Proxy} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";

contract MockTransactionRelayer is TransactionRelayer {
    function entryPoint(address target, uint256 _value) public {
        internalCall(target, _value);
    }

    function internalCall(address target, uint256 _value) internal {
        bool success = false;
        assembly {
            success := call(
            gas(),
            target,
            _value,
            0,
            0,
            0,
            0
            )
        }
        require(success, "call to target reverted");
    }
}

contract TransactionRelayerTest is Test {
    address implementation;
    MockTransactionRelayer transactionRelayer;

    function setUp() public {
        implementation = address(new MockTransactionRelayer());
        // bytes memory data = abi.encodeCall(TransactionRelayer.initialize, "");
        address proxy = address(new ERC1967Proxy(implementation, ""));
        transactionRelayer = MockTransactionRelayer(proxy);
    }

    function test_transactionRelayer() public {
        transactionRelayer.initialize();

        //@audit-info => Not possible to fund native to the TransactionRelayer
        vm.expectRevert();
        (bool success, ) = address(transactionRelayer).call{value: 1 ether}("");
        require(success);

        assertEq(address(transactionRelayer).balance, 0);

        //@audit-info => Not possible to transfer out native from the TransactionRelayer
        address user1 = makeAddr("user1");
        vm.expectRevert();
        transactionRelayer.entryPoint(user1, 1 ether);

        //@audit-info => Not possible to send native in the call because not payable modifier
        // transactionRelayer.entryPoint{value: 1 ether}(user1, 1 ether);
    }
}
```

**Recommended Mitigation:** Either make the function `executeByInvestorWithBlockLimit` payable or add the `receive` to allow the Relayer to be funded separately and allow `executeByInvestorWithBlockLimit` to spend from that balance.

Alternatively, remove the `value` parameter from the signature and from the `params[]` so that the external call explicitly never transfers natively to the destination address.

**Securitize:** `TransactionRelayer` has been significantly changed such that `executeByInvestorWithBlockLimit` and most other functions now always revert since they were deprecated. The only remaining working function is `executePreApprovedTransaction` which doesn't take a `value` parameter nor send native.

**Cyfrin:** Verified.

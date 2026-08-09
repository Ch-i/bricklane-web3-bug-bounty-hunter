---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-kleidi-report-0-21
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-kleidi-report
title: '[L-22] `removeCalldataCheckDatahash` could mistakenly remove a wildcard check
  if the wildcard check is added with an empty `dataHash`'
vuln_class: []
---

# [L-22] `removeCalldataCheckDatahash` could mistakenly remove a wildcard check if the wildcard check is added with an empty `dataHash`

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Kleidi_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md)_

---

**Impact**

`_addCalldataCheck` doesn't enforce that a wildcard check has no `dataHashes`

https://github.com/solidity-labs-io/kleidi/blob/1a06ac16bc99d0b4081281329d03064c3737f5e4/src/Timelock.sol#L1062-L1112

```solidity
    function _addCalldataCheck(
        address contractAddress,
        bytes4 selector,
        uint16 startIndex,
        uint16 endIndex,
        bytes[] memory data,
        bool[] memory isSelfAddressCheck
    ) private {
        require(
            contractAddress != address(0),
            "CalldataList: Address cannot be zero"
        );
        require(selector != bytes4(0), "CalldataList: Selector cannot be empty");
        require(
            startIndex >= 4, "CalldataList: Start index must be greater than 3"
        );
        require(
            data.length == isSelfAddressCheck.length,
            "CalldataList: Array lengths must be equal"
        );
        /// prevent misconfiguration where a hot signer could change timelock
        /// or safe parameters
        require(
            contractAddress != address(this),
            "CalldataList: Address cannot be this"
        );
        require(contractAddress != safe, "CalldataList: Address cannot be safe");

        Index[] storage calldataChecks =
            _calldataList[contractAddress][selector];
        uint256 listLength = calldataChecks.length;
        /// @audit If you add wildcard, you need to remove it before adding something else
        if (listLength == 1) {
            require(
                calldataChecks[0].startIndex != calldataChecks[0].endIndex,
                "CalldataList: Cannot add check with wildcard"
            );
        }

        if (startIndex == endIndex) {
            require(
                startIndex == 4,
                "CalldataList: End index eqauls start index only when 4"
            );
            require(
                listLength == 0,
                "CalldataList: Add wildcard only if no existing check"
            );

            /// @audit Add `data.length == 0` so you ensure this check is correct
        } else {
```

A Wildcard Could be added with Data by mistakes due to a lack of this check

In removing the dataHash, the wildcard would also be removed by `removeCalldataCheckDatahash`:

https://github.com/solidity-labs-io/kleidi/blob/1a06ac16bc99d0b4081281329d03064c3737f5e4/src/Timelock.sol#L903-L908

```solidity
    function removeCalldataCheckDatahash(
        address contractAddress,
        bytes4 selector,
        uint256 index,
        bytes32 dataHash
    ) external onlyTimelock {
```

**Proof Of Concept**

You can pass an empty string and the check will pass, please see this test which shows:
- Setup the check with empty bytes
- Remove the empty bytes
- Removes the wildcard check

forge test --match-test test_show_arbitraryCheck -vv

```solidity
 function test_show_arbitraryCheck() public {
        address[] memory targetAddresses = new address[](1);
        targetAddresses[0] = address(lending);

        bytes4[] memory selectors = new bytes4[](1);
        selectors[0] = MockLending.deposit.selector;

        /// compare first 20 bytes
        uint16[] memory startIndexes = new uint16[](1);
        startIndexes[0] = 4;

        uint16[] memory endIndexes = new uint16[](1);
        endIndexes[0] = 4;

        bytes[][] memory checkedCalldatas = new bytes[][](1);
        bytes[] memory checkedCalldata1 = new bytes[](1);
        checkedCalldata1[0] = hex"";
        checkedCalldatas[0] = checkedCalldata1;

        bool[][] memory isSelfAddressChecks = new bool[][](1);
        bool[] memory isSelfAddressCheck = new bool[](1);
        isSelfAddressCheck[0] = false;
        isSelfAddressChecks[0] = isSelfAddressCheck;

        vm.prank(address(timelock));
        timelock.addCalldataChecks(
            targetAddresses,
            selectors,
            startIndexes,
            endIndexes,
            checkedCalldatas,
            isSelfAddressChecks
        );

        // Check that the check is there
        timelock.checkCalldata(targetAddresses[0], abi.encodePacked(selectors[0]));

        // Remove it
        vm.prank(address(timelock));
        timelock.removeCalldataCheck(targetAddresses[0], selectors[0], 0);

        // Show that now it reverts
        vm.expectRevert();
        timelock.checkCalldata(targetAddresses[0], abi.encodePacked(selectors[0]));
    }
```



**Mitigation**

Add a check to enforce that data.length is 0 for wildcard checks

```solidity
        if (startIndex == endIndex) {
            require(
                startIndex == 4,
                "CalldataList: End index eqauls start index only when 4"
            );
            require(
                listLength == 0,
                "CalldataList: Add wildcard only if no existing check"
            );

            /// @audit Add `data.length == 0` so you ensure this check is correct
```

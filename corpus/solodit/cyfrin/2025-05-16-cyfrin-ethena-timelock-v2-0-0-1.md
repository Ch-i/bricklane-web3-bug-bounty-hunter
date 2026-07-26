---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-16-cyfrin-ethena-timelock-v2-0-0-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-05-16T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-16-cyfrin-ethena-timelock-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-16-cyfrin-ethena-timelock-v2-0
title: Re-entrancy protection can be evaded via `TimelockController::executeBatch`
vuln_class: []
---

# Re-entrancy protection can be evaded via `TimelockController::executeBatch`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-16-cyfrin-ethena-timelock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-16-cyfrin-ethena-timelock-v2.0.md)_

---

**Description:** `EthenaTimelockController::execute` overrides `TimelockController::execute` and adds a `nonReentrant` modifier to prevent re-entrant calls back into it.

However `TimelockController::executeBatch` is not overridden so re-entrancy can still occur that way. Beyond the re-entrancy evasion this doesn't appear further exploitable.

**Proof Of Concept:**
In `test/EthenaTimelockController.t.sol`, change `MaliciousReentrant::maliciousExecute` to:
```solidity
function maliciousExecute() external {
    if (!reentered) {
        reentered = true;
        // re-enter the timelock through executeBatch
        bytes memory data = abi.encodeWithSignature("maliciousFunction()");
        address[] memory targets = new address[](1);
        targets[0] = address(this);
        uint256[] memory values = new uint256[](1);
        values[0] = 0;
        bytes[] memory payloads = new bytes[](1);
        payloads[0] = data;
        timelock.executeBatch(targets, values, payloads, bytes32(0), bytes32(0));
    }
}
```

Then run the relevant test: `forge test --match-test testExecuteWhitelistedReentrancy -vvv` and see that the test fails because the expected re-entrancy error no longer gets thrown.

**Recommended Mitigation:** Override `TimelockController::executeBatch` in `EthenaTimelockController` to add `nonReentrant` modifier then call the parent function.

**Ethena:** Fixed in commit [89d4190](https://github.com/ethena-labs/timelock-contract/commit/89d41901be3387c11c2150c19eb99883ed807d79#diff-8ca72e61ebf9a693737b5c9052aa3814e8b291e3d6dd0341fe88b5b5e781427bR147).

**Cyfrin:** Verified.

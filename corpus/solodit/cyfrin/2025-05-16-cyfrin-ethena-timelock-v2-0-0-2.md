---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-16-cyfrin-ethena-timelock-v2-0-0-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-05-16T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-16-cyfrin-ethena-timelock-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-16-cyfrin-ethena-timelock-v2-0
title: '`TimelockController` won''t revert when executing on non-existent contracts'
vuln_class: []
---

# `TimelockController` won't revert when executing on non-existent contracts

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-16-cyfrin-ethena-timelock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-16-cyfrin-ethena-timelock-v2.0.md)_

---

**Description:** `TimelockController::_execute` does this:
```solidity
function _execute(address target, uint256 value, bytes calldata data) internal virtual {
    (bool success, bytes memory returndata) = target.call{value: value}(data);
    Address.verifyCallResult(success, returndata);
}
```

If `target` is a non-existent contract but `data` contains a valid expected function call with parameters, the `call` will return `true`; `Address.verifyCallResult` fails to catch this case.

**Proof Of Concept:**
Add PoC function to `test/EthenaTimelockController.sol`:
```solidity
function testExecuteNonExistentContract() public {
    bytes memory data = abi.encodeWithSignature("DONTEXIST()");
        _scheduleWaitExecute(address(0x1234), data);
}
```

Run with: `forge test --match-test testExecuteNonExistentContract -vvv`

**Recommended Mitigation:** We reported this bug to OpenZeppelin but they said they prefer the current implementation as it is more flexible. We disagree with this assessment and believe it is incorrect for `TimelockController::_execute` to not revert when there is valid calldata but the target has no code.

**Ethena:** Fixed in commit [e58c547](https://github.com/ethena-labs/timelock-contract/commit/e58c547e3bcbea79d9df7121b5bb04626a2b72e0#diff-8ca72e61ebf9a693737b5c9052aa3814e8b291e3d6dd0341fe88b5b5e781427bR191-R197) by overriding `_execute` to revert if `data.length > 0 && target.code.length == 0`.

**Cyfrin:** Verified.

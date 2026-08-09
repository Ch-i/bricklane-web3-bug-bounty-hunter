---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-16-cyfrin-ethena-timelock-v2-0-0-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-05-16T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-16-cyfrin-ethena-timelock-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-16-cyfrin-ethena-timelock-v2-0
title: '`EthenaTimelockController::addToWhitelist` and `removeFromWhitelist` don''t
  revert for non-existent `target` address'
vuln_class: []
---

# `EthenaTimelockController::addToWhitelist` and `removeFromWhitelist` don't revert for non-existent `target` address

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-16-cyfrin-ethena-timelock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-16-cyfrin-ethena-timelock-v2.0.md)_

---

**Description:** `EthenaTimelockController::addToWhitelist` and `removeFromWhitelist` should revert if the `target` address doesn't exist (has no code).

**Proof of Concept:** Add PoC function to `test/EthenaTimelockController.t.sol`:
```solidity
function testAddNonExistentContractToWhitelist() public {
    bytes memory addToWhitelistData = abi.encodeWithSignature(
        "addToWhitelist(address,bytes4)", address(0x1234), bytes4(keccak256("DONTEXIST()"))
    );
    _scheduleWaitExecute(address(timelock), addToWhitelistData);
}
```

Run with: `forge test --match-test testAddNonExistentContractToWhitelist -vvv`

**Recommended Mitigation:** Revert if `target.code.length == 0`.

**Ethena:** Fixed in commit [89d4190](https://github.com/ethena-labs/timelock-contract/commit/89d41901be3387c11c2150c19eb99883ed807d79#diff-8ca72e61ebf9a693737b5c9052aa3814e8b291e3d6dd0341fe88b5b5e781427bR6-R76) to not allow whitelisting of targets with no code.

**Cyfrin:** Verified.

\clearpage

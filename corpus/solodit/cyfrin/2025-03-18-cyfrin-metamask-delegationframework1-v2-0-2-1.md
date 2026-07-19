---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-2-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-03-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-18-cyfrin-metamask-delegationframework1-v2-0
title: '`AllowedCalldataEnforcer` cannot authenticate empty calldata preventing `receive()`
  function calls'
vuln_class: []
---

# `AllowedCalldataEnforcer` cannot authenticate empty calldata preventing `receive()` function calls

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md)_

---

**Description:** The `AllowedCalldataEnforcer` contract has a design flaw that prevents it from authenticating calls with empty calldata. This issue arises from a requirement check in the `getTermsInfo` function that enforces `_terms.length >= 33`:

```solidity
// AllowedCalldataEnforcer.sol
    function getTermsInfo(bytes calldata _terms) public pure returns (uint256 dataStart_, bytes memory value_) {
>>      require(_terms.length >= 33, "AllowedCalldataEnforcer:invalid-terms-size");
        dataStart_ = uint256(bytes32(_terms[0:32]));
        value_ = _terms[32:];
    }
```

The first 32 bytes represent the starting offset in the calldata, and anything after that represents the expected value to match against. This design requires at least 1 byte for the value, which prevents the enforcer from handling empty calldata scenarios.

Ethereum contracts can receive ETH through functions with empty calldata, specifically:
- When calling a contract's `receive()` function, which requires empty calldata
- When making simple ETH transfers to contracts that implement `receive()`

**Impact:** Users cannot use `AllowedCalldataEnforcer` to authorize delegations that should only permit simple ETH transfers to contracts with receive(). Common use cases like depositing ETH to WETH (which uses the receive() function) cannot be properly enforced through this caveat


**Recommended Mitigation:** Consider modifying the `getTermsInfo` function to allow terms of exactly 32 bytes length, treating it as a special case where the value is empty:

```solidity
function getTermsInfo(bytes calldata _terms) public pure returns (uint256 dataStart_, bytes memory value_) {
    require(_terms.length >= 32, "AllowedCalldataEnforcer:invalid-terms-size");
    dataStart_ = uint256(bytes32(_terms[0:32]));
    if (_terms.length == 32) {
        value_ = new bytes(0); // @audit Empty bytes for empty calldata
    } else {
        value_ = _terms[32:];
    }
}
```

**Metamask:** Addressed in commit [db11bf7](https://github.com/MetaMask/delegation-framework/commit/db11bf74034a94bddaae189299cb757fd03cadeb).

**Cyfrin:** Resolved. Added a new caveat `ExactCalldataEnforcer` to address the issue.

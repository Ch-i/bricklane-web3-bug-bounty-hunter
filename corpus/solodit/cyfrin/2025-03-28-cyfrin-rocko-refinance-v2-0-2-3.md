---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-28-cyfrin-rocko-refinance-v2-0-2-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-03-28T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-28-cyfrin-rocko-refinance-v2-0
title: Prevent repetitive hashing of identical strings
vuln_class: []
---

# Prevent repetitive hashing of identical strings

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-28-cyfrin-rocko-refinance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md)_

---

**Description:** `RockoFlashRefinance::_compareStrings` is often called with the same values resulting in duplicate unnecessary work. A simple and more efficient way to prevent this is by first performing the conversion using `_parseProtocol` for both `from`/`to` inputs then simply comparing the enums as needed in functions like `refinance` and `_revokeTokenSpendApprovals`.

If string comparisons are required:
* hard-code the hash result as `bytes32` constants for common expected strings such as "aave", "morpho", "compound" and using these hard-coded constants inside `_parseProtocol` and other functions
* in functions such as `RockoFlashRefinance::refinance`, cache the hash of the `from`/`to` inputs in local `bytes32` variables and use the cached hashes and the hard-coded constants for the comparisons

One simple way to achieve this is by:
* defining a function to return the hash of a string:
```solidity
    function _hashString(string calldata input) private pure returns (bytes32 output) {
        output = keccak256(bytes(input));
    }
```
* changing `_compareStrings` to take two `bytes32` as input:
```solidity
    function _compareStrings(bytes32 a, bytes32 b) private pure returns (bool) {
        return a == b;
    }
```

Consider OpenZeppelin's string equality [implementation](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/Strings.sol#L134-L136) as well.

**Rocko:** Fixed in commit [a59ba0e](https://github.com/getrocko/onchain/commit/a59ba0e7958c544ad95788ce29923a342a2ea35a).

**Cyfrin:** Verified.

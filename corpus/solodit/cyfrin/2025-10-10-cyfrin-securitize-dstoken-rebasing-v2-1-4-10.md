---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-4-10
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: More efficient way of comparing two strings for equality in `CommonUtils::isEqualString`
vuln_class: []
---

# More efficient way of comparing two strings for equality in `CommonUtils::isEqualString`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** More efficient way of comparing two strings for equality in `CommonUtils::isEqualString` [from](https://github.com/Vectorized/solady/blob/main/src/utils/g/LibString.sol#L858-L863) Solady:
```solidity
  function isEqualString(string memory a, string memory b) internal pure returns (bool result) {
      /// @solidity memory-safe-assembly
      assembly {
          result := eq(keccak256(add(a, 0x20), mload(a)), keccak256(add(b, 0x20), mload(b)))
      }
  }
```

**Securitize:** Acknowledged.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-18-cyfrin-linea-forced-txns-v2-0-2-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-06-18T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-18-cyfrin-linea-forced-txns-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-18-cyfrin-linea-forced-txns-v2-0
title: More efficient usage of `LibRLP` in `ForcedTransactionGateway::_buildAccessList,
  submitForcedTransaction `
vuln_class: []
---

# More efficient usage of `LibRLP` in `ForcedTransactionGateway::_buildAccessList, submitForcedTransaction `

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-18-cyfrin-linea-forced-txns-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-18-cyfrin-linea-forced-txns-v2.0.md)_

---

**Description:** A more efficient implementation of `ForcedTransactionGateway::_buildAccessList` avoids:
* empty initialization of `acct` (see this [comment](https://github.com/Vectorized/solady/blob/main/src/utils/LibRLP.sol#L108))
* calling `LibRLP.p()` since it does [nothing](https://github.com/Vectorized/solady/blob/main/src/utils/LibRLP.sol#L101)
```solidity
   function _buildAccessList(AccessList[] memory _accessList) internal pure returns (LibRLP.List memory list) {
    unchecked {
      // list is already zero-initialized (empty list)
      for (uint256 i; i < _accessList.length; ++i) {
        LibRLP.List memory keys;  // Empty list, no p() needed
        bytes32[] memory ks = _accessList[i].storageKeys;
        for (uint256 j; j < ks.length; ++j) {
          bytes memory b = new bytes(32);
          assembly {
            mstore(add(b, 0x20), mload(add(ks, add(0x20, shl(5, j)))))
          }
          keys = LibRLP.p(keys, b);
        }
        LibRLP.List memory acct = LibRLP.p(_accessList[i].contractAddress);  // single-arg overload
        acct = LibRLP.p(acct, keys);
        list = LibRLP.p(list, acct);
      }
    }
  }
```

The same techniques can be used in `ForcedTransactionGateway::submitForcedTransaction`:
```diff
-   LibRLP.List memory transactionFieldList = LibRLP.p();
-   transactionFieldList = LibRLP.p(transactionFieldList, DESTINATION_CHAIN_ID);
+   LibRLP.List memory transactionFieldList = LibRLP.p(DESTINATION_CHAIN_ID);
```

**Linea:** Fixed in commit [857c4b7](https://github.com/Consensys/linea-monorepo/pull/2297/changes/857c4b76c90244bf8c5c8bd66c0f74726ce0cd6b#diff-8d8766008f6ce77c606b66562a607209e5227fa45ae395a762f75d474ef17670L128-R230).

**Cyfrin:** Verified.

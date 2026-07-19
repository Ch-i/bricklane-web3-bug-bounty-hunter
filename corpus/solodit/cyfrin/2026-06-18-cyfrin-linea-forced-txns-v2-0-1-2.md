---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-18-cyfrin-linea-forced-txns-v2-0-1-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-06-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-18-cyfrin-linea-forced-txns-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-18-cyfrin-linea-forced-txns-v2-0
title: Remove TODO comments
vuln_class: []
---

# Remove TODO comments

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-18-cyfrin-linea-forced-txns-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-18-cyfrin-linea-forced-txns-v2.0.md)_

---

**Description:** Remove TODO comments:
```solidity
rollup/LineaRollupBase.sol
124:  // TODO check the layout of these variables
```

Comparing this audit's `LineaRollup` storage layout to the previous "mixed upgrade" version using `forge inspect -R "@openzeppelin/=contracts/node_modules/@openzeppelin/" --hardhat --evm-version cancun LineaRollup storageLayout` shows that the new storage slots are appended after the previously existing `shnarfProvider` slot which is correct:
```shell
  Name                            | Type                        | Slot | Offset | Bytes
=======================================================================================
# identical
  shnarfProvider                  | contract IProvideShnarf     | 449  | 0      | 20

# new, over-write previous gap
  nextForcedTransactionNumber     | uint256                     | 450  | 0      | 32
  forcedTransactionL2BlockNumbers | mapping(uint256 => uint256) | 451  | 0      | 32
  forcedTransactionRollingHashes  | mapping(uint256 => bytes32) | 452  | 0      | 32
  forcedTransactionFeeInWei       | uint256                     | 453  | 0      | 32
  addressFilter                   | contract IAddressFilter     | 454  | 0      | 20

# pushed down 5 slots
  __gap_LineaRollup               | uint256[50]                 | 455  | 0      | 1600
  __gap_LivenessRecoveryOperator  | uint256[50]                 | 505  | 0      | 1600
```

The storage gap `LineaRollupBase::__gap_LineaRollup` has not been reduced but this appears to be safe since it is still at the end of the storage layout.

**Linea:** Fixed in commit [857c4b7](https://github.com/Consensys/linea-monorepo/pull/2297/changes/857c4b76c90244bf8c5c8bd66c0f74726ce0cd6b#diff-99ffaedf2a0a7fba64bba5cb2ae2ad8c1587960f6cf5104f3e12f67a5c7d38d8L124).

**Cyfrin:** Verified.

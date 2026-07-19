---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-5-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: QA/Gas improvements in related Sablier contracts
vuln_class: []
---

# QA/Gas improvements in related Sablier contracts

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** While technically outside the scope of this audit, we also had to read and understand other related Sablier contracts as the in-scope contracts inherit from them. Here is a collection of QA/gas findings from these contracts.

* use [SafeTransferLib::safeTransferETH](https://github.com/Vectorized/solady/blob/main/src/utils/SafeTransferLib.sol#L95-L103) instead of Solidity `call` to send ETH - `Comptrollerable::transferFeesToComptroller`. Alternatively use a low-level call patterns such as:
```solidity

```diff
-        (bool success,) = address(comptroller).call{ value: feeAmount }("");
+        bool success;
+        address feeReceiver = comptroller;
+        assembly { success := call(gas(), feeReceiver, feeAmount, 0, 0, 0, 0) }
```

* cache storage to prevent identical storage reads - `Comptrollerable::transferFeesToComptroller`

* [cheaper](https://github.com/devdacian/solidity-gas-optimization?tab=readme-ov-file#6-dont-cache-calldata-length-effective-009-cheaper) not to cache `calldata` length - `Batch::batch`

* in Solidity don't initialize to default values - `Batch::batch`

**Sablier:** Fixed the second point in commit [0a5ed9d](https://github.com/sablier-labs/lockup/commit/0a5ed9d1f6b3fa258be9de1129fa533ba2620725), acknowledging the rest.

**Cyfrin:** Verified.

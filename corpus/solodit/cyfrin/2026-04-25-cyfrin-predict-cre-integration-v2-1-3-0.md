---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-25-cyfrin-predict-cre-integration-v2-1-3-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-04-25T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-25-cyfrin-predict-cre-integration-v2-1
title: Cache storage array length
vuln_class: []
---

# Cache storage array length

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-25-cyfrin-predict-cre-integration-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md)_

---

**Description:** Several loops in `ChainlinkUpDownAdapter` and `ChainlinkReceiverBase` read `.length` repeatedly; `_processReport` iterates over CRE batches every 30s, making the savings material.

```solidity
ChainlinkUpDownAdapter.sol
228:        for (uint256 i = 0; i < chainlinkReports.length; i++) {
241:        for (uint256 i = 0; i < chainlinkReports.length; i++) {
```

**Impact:** Wasted gas per iteration on every CRE cron tick; compounds with batch size.

**Recommended Mitigation:**
```solidity
uint256 len = chainlinkReports.length;
for (uint256 i; i < len; i++) {
    // body
}
```

**Predict.fun:** Fixed in commit [2ca1146](https://github.com/PredictDotFun/prediction-market/commit/2ca1146ccb9227de45438e17e3d95fa08d48490b).

**Cyfrin:** Verified.

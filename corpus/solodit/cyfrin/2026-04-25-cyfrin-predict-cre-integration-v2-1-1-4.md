---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-25-cyfrin-predict-cre-integration-v2-1-1-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-04-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-25-cyfrin-predict-cre-integration-v2-1
title: Inconsistent expiry comparison between CRE pre-flight and onchain validation
vuln_class: []
---

# Inconsistent expiry comparison between CRE pre-flight and onchain validation

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-25-cyfrin-predict-cre-integration-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md)_

---

**Description:** The CRE off-chain workflow and the onchain adapter apply asymmetric expiry checks on Data Streams reports.

The CRE check in `fetchDataStreamsReportsBulk.ts:93-95` uses strict less-than:

```typescript
if (decodedData.expiresAt < nowSeconds) {
    throw new Error(`Report expired for ${report.feedID}...`);
}
```

This **accepts** a report when `expiresAt == nowSeconds`. Onchain, `ChainlinkUpDownAdapter.sol:354` uses greater-than-or-equal:

```solidity
if (block.timestamp >= expiresAt) {
    revert ChainlinkAdapter__ReportExpired();
}
```

This **rejects** when `block.timestamp == expiresAt`.

Between the CRE DON validating a report and the resulting transaction being mined on BSC (~3 second blocks + Keystone Forwarder pipeline latency ≈ 6-15 seconds), `block.timestamp` advances beyond the CRE's `nowSeconds`. Any report where `expiresAt - nowSeconds < pipeline_latency` passes CRE validation but reverts onchain.

These are semantically mismatched.

**Impact:** In practice this is harmless (the tx will revert) and Chainlink DON sets `expiresAt` hours/days ahead of `observationsTimestamp`, so the 1-second boundary gap is unreachable. The on-chain check remains authoritative regardless.

**Recommended Mitigation:** Align CRE expiry check with on-chain semantics (`<= ` instead of `<`) for consistency.

```typescript
//fetchDataStreamsReportsBulk.ts:94

    if (decodedData.expiresAt <= nowSeconds) {
      throw new Error(`Report expired for ${report.feedID}: expiresAt=${decodedData.expiresAt}, now=${nowSeconds}`);
    }
```

**Predict.fun:** Fixed in commit [53138ab](https://github.com/PredictDotFun/prediction-market/pull/71/changes/53138ab7de899b9e250226dc0f1b925fb68a51cc).

**Cyfrin:** Verified.

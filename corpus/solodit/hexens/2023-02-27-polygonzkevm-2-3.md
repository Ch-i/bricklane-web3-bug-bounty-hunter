---
affected_contracts: []
derives_from: []
id: solodit-hexens-2023-02-27-polygonzkevm-2-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-02-27T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-02-27-PolygonZkEvm.md
tags:
- firm:hexens
- report:2023-02-27-polygonzkevm
title: 10. LOOP OPTIMISATION
vuln_class: []
---

# 10. LOOP OPTIMISATION

_Section severity (from Solodit section header): Low_  
_Audit firm: Hexens_  
_Source report: [2023-02-27-PolygonZkEvm.md](https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-02-27-PolygonZkEvm.md)_

---

**Severity:** Low

**Path:** PolygonZkEvm.sol

**Description:** 

In the function updateBatchFee the function calculates number of blocks that were verified above and below the verification time target. The fee is updated based corresponding to their ratio.

The loop that checks for targets that are above the target does a backward loop from the newly verified batch up to the last verified batch, it does it until it reaches the last verified batch traversing all of the sequences in between. The loop can be optimised as the sequencedTimestamp's are strictly growing and from the first time that a sequence is found that is above the target time, the rest of the batches up until the last verified batch can be considered to be verified above the target (as every next sequencedTimestamp will be smaller than the current).

An optimisation will be to account all of the batches up until the last verified batch and break out of the loop as soon as such a sequence is met.

*PolygonZkEvm.sol*
```
function _updateBatchFee(uint64 newLastVerifiedBatch) internal {
   uint64 currentLastVerifiedBatch = getLastVerifiedBatch();
   uint64 currentBatch = newLastVerifiedBatch;uint256 totalBatchesAboveTarget;
uint256 newBatchesVerified = newLastVerifiedBatch -
   currentLastVerifiedBatch;

while (currentBatch != currentLastVerifiedBatch) {
   // Load sequenced batchdata
   SequencedBatchData
       storage currentSequencedBatchData = sequencedBatches[
           currentBatch
       ];

   // Check if timestamp is above or below the VERIFY_BATCH_TIME_TARGET
   if (
       block.timestamp - currentSequencedBatchData.sequencedTimestamp >
       veryBatchTimeTarget
   ) {
       totalBatchesAboveTarget +=
           currentBatch -
           currentSequencedBatchData.previousLastBatchSequenced;   //AUDIT: change to currentBatch - currentLastVerifiedBatch and break out of the loop
   }

   // update currentLastVerifiedBatch
   currentBatch = currentSequencedBatchData.previousLastBatchSequenced;
}
```
**Remediation:** The totalBatchesAboveTarget can be incremented by currentBatch - currentLastVerifiedBatch and after that the loop should break.

**Status:** Fixed

- - -

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-24-cyfrin-linea-3-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-05-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md
tags:
- firm:cyfrin
- report:2024-05-24-cyfrin-linea
title: Add sanity check to `LineaRollup::submitBlobs` to ensure all blobs are validated
vuln_class: []
---

# Add sanity check to `LineaRollup::submitBlobs` to ensure all blobs are validated

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-24-cyfrin-linea.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md)_

---

**Description:** In `LineaRollup::submitBlobs`, if `_blobSubmissionData.length` is smaller than the actual number of attached blobs the code will successfully execute and store an intermediate value to `shnarfFinalBlockNumbers[computedShnarf]` because the `for` loop did not iterate through all the blobs.

To prevent this edge-case from occurring add an early fail sanity check before the `for` loop eg:
```solidity
if(blobhash(blobSubmissionLength) != EMPTY_HASH) {
      revert MoreBlobsThanData();
}
```

**Linea:**
Acknowledged; will be resolved in a future release focused on decentralization. Currently the Operator Service is written in such a way this cannot happen, and there is always a 1:1 mapping of data:blob.

\clearpage

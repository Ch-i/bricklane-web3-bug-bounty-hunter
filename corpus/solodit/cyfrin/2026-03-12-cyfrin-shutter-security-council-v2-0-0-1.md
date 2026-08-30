---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-12-cyfrin-shutter-security-council-v2-0-0-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-12-cyfrin-shutter-security-council-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-12-cyfrin-shutter-security-council-v2-0
title: '`_getProposalTxHashes` can be simplified'
vuln_class: []
---

# `_getProposalTxHashes` can be simplified

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-12-cyfrin-shutter-security-council-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-12-cyfrin-shutter-security-council-v2.0.md)_

---

**Description:** `SecurityCouncilAzorius._getProposalTxHashes` retrieves the `txHashes` for a given `proposalId` by calling `Azorius.getProposal` and only using the second return value. However, `Azorius` already exposes a dedicated view function, `getProposalTxHashes`, which directly returns the `txHashes`.

**Recommended Mitigation:** Use `Azorius.getProposalTxHashes()` instead. This requires adding `getProposalTxHashes()` to the `IAzorius` interface.

```diff
    function _getProposalTxHashes(uint32 proposalId) internal view returns (bytes32[] memory txHashes) {
-       (, txHashes,,,) = IAzorius(azorius).getProposal(proposalId);
+       txHashes = IAzorius(azorius).getProposalTxHashes(proposalId);
    }
```

**Blockful:** Fixed in commit [d7e96b2](https://github.com/blockful/shutter-security-council/commit/d7e96b262204998bc90cab850f8221e955a1391c#diff-f8e3fe7aff7a5528b681495716238afa73895a423f8032270280e77ff3dd52ad)

**Cyfrin:** Verified.

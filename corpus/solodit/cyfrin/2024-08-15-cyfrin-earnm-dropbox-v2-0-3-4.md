---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-3-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: '`VRFHandler` shouldn''t inherit from `ConfirmedOwner` since it inherits from
  `VRFConsumerBaseV2Plus` which already inherits from `ConfirmedOwner`'
vuln_class: []
---

# `VRFHandler` shouldn't inherit from `ConfirmedOwner` since it inherits from `VRFConsumerBaseV2Plus` which already inherits from `ConfirmedOwner`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** `VRFHandler` shouldn't inherit from `ConfirmedOwner` since it inherits from `VRFConsumerBaseV2Plus` which already [inherits](https://github.com/smartcontractkit/chainlink/blob/develop/contracts/src/v0.8/vrf/dev/VRFConsumerBaseV2Plus.sol#L101) from `ConfirmedOwner`:
```diff
- contract VRFHandler is ConfirmedOwner, VRFConsumerBaseV2Plus, IVRFHandler {
+ contract VRFHandler is VRFConsumerBaseV2Plus, IVRFHandler {
```

**Mode:**
Fixed in commit [7fe63a3](https://github.com/Earnft/dropbox-smart-contracts/commit/7fe63a32d61adf53ad722a24928f855b68626618).

**Cyfrin:** Verified.

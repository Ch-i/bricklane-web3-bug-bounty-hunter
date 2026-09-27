---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-10-tokentable-fractionalizer-and-sellnow-1-3
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-04-10T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-10-TokenTable-Fractionalizer-and-SellNow.md
tags:
- firm:codespect
- report:2025-04-10-tokentable-fractionalizer-and-sellnow
title: '[H-04] approved segments don’t reset their approval after being transferred'
vuln_class: []
---

# [H-04] approved segments don’t reset their approval after being transferred

_Section severity (from Solodit section header): High_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-10-TokenTable-Fractionalizer-and-SellNow.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-10-TokenTable-Fractionalizer-and-SellNow.md)_

---

**Files:** [ShareFractionalizer.sol](https://github.com/EthSign/tokentable-sellnow-ft-fractionalizer-evm/blob/076d70abad50c2dddf8c5324c98d72f68ec6dc72/src/ShareFractionalizer.sol)

**Description:**

The `approve(...)` function gives permission to a trusted operator to be able to transfer the selected user's segments. This delegation of authority is considered secure because the user specifically selects who becomes an operator and for which of his segments.

However, if the segments get transferred through `updateShareSegmentsAdmin(...)` by the owner or `transferShareSegments(...)` by the user, the operator of those segments remains the same.

The `transferFrom(...)` function doesn't account for this scenario, allowing an operator to transfer segments that he was previously approved for by the previous owner:

```solidity
function transferFrom(address from, address to, uint256[] calldata segmentIDs) external {
    for (uint256 i = 0; i < segmentIDs.length; i++) {
        // has to be approved to transfer the segment
        require(
            operators[from][segmentIDs[i]] == _msgSender() || isApprovedForAll[from][_msgSender()], InvalidAccess()
        );
        // cannot transfer segments that are already claimed
        require(segments[segmentIDs[i]].claimableAmount != 0, SegmentAlreadyClaimed());
        // clear approval
        operators[from][segmentIDs[i]] = address(0);
        segments[segmentIDs[i]].recipient = to;
    }
}
```

The issue arises from the fact that the operator of a segment doesn't get reset when `updateShareSegmentsAdmin(...)` or `transferShareSegments(...)` is called.

**Impact:** A malicious user can always set himself as the operator of his segments and regain access to them in the case owner calls `updateShareSegmentsAdmin(...)` or possibly sells/has to transfer his segments to another address.

**Recommendation(s):** Set the operator to `address(0)` after changing a segment's recipient in `updateShareSegmentsAdmin(...)` and `transferShareSegments(...)`.

**Status:** Fixed

**Update from TokenTable:** [3f3a670c0f67983a0dd3acbec5e0eeee11e1806d](https://github.com/EthSign/tokentable-sellnow-ft-fractionalizer-evm/pull/13/commits/3f3a670c0f67983a0dd3acbec5e0eeee11e1806d)

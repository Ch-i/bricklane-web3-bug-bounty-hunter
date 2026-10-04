---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-10-tokentable-fractionalizer-and-sellnow-0-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-04-10T00:00:00Z'
related_swc: []
severity: Critical
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-10-TokenTable-Fractionalizer-and-SellNow.md
tags:
- firm:codespect
- report:2025-04-10-tokentable-fractionalizer-and-sellnow
title: '[C-01] isApprovedForAll mapping allows arbitrary transfer of any segment'
vuln_class: []
---

# [C-01] isApprovedForAll mapping allows arbitrary transfer of any segment

_Section severity (from Solodit section header): Critical_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-10-TokenTable-Fractionalizer-and-SellNow.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-10-TokenTable-Fractionalizer-and-SellNow.md)_

---

**Files:** [ShareFractionalizer.sol](https://github.com/EthSign/tokentable-sellnow-ft-fractionalizer-evm/blob/076d70abad50c2dddf8c5324c98d72f68ec6dc72/src/ShareFractionalizer.sol#L207)

**Description:**

The `setApprovalForAll(...)` function is intended to allow a trusted operator to manage *all* of a user's segments. While an operator cannot claim a user's segment (i.e., receive token distribution), they are allowed to transfer segments to arbitrary recipients. Since the user explicitly chooses the operator, this is assumed to be a trusted delegation.

However, the `transferFrom(...)` function contains a flawed access control check:

```solidity
function transferFrom(address from, address to, uint256[] calldata segmentIDs) external {
    for (uint256 i = 0; i < segmentIDs.length; i++) {
        // has to be approved to transfer the segment
        require(
            operators[from][segmentIDs[i]] == _msgSender() || isApprovedForAll[from][_msgSender()],
            InvalidAccess() // @audit-issue: no relation to specific segmentID
        );
        // cannot transfer segments that are already claimed
        require(segments[segmentIDs[i]].claimableAmount != 0, SegmentAlreadyClaimed());
        // clear approval
        operators[from][segmentIDs[i]] = address(0);
        segments[segmentIDs[i]].recipient = to;
    }
}
```

The first `require` checks whether `msg.sender` is either:

- Approved for a specific segment via `operators[from][segmentID]`, or;
- Approved for all of the user's segments via `isApprovedForAll[from][msg.sender]`;

The issue is with the second condition: `isApprovedForAll[from][msg.sender]` is a global flag and does not validate that the segment in question actually belongs to `from`. This means `msg.sender` can transfer any segment—even if `from` is not the original owner of that segment—as long as the global approval flag is set.

**Impact:** An attacker can exploit this logic to transfer *any* active segment (i.e., those with non-zero claimable tokens) from *any* user who has granted them global approval. This effectively allows the theft of all future token distributions tied to those segments.

**Recommendation:** Modify the access control check to ensure that each `segmentID` being transferred is indeed owned by the `from` address.

**Status:** Fixed

**Update from TokenTable:** [ecdf862821b03307ef07940a8c7097f8803cbdb7](https://github.com/EthSign/tokentable-sellnow-ft-fractionalizer-evm/pull/13/commits/ecdf862821b03307ef07940a8c7097f8803cbdb7)

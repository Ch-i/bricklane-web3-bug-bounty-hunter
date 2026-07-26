---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-1-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: Any slasher can increase another one's reveal delays
vuln_class: []
---

# Any slasher can increase another one's reveal delays

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** Commits in `RLN` are made as follows:
```solidity
function slashCommit(address account, bytes32 hash) external onlyRole(SLASHER_ROLE) {
    uint256 lastReveal = lastRevealStartTime[account];
    uint256 revealStartTime;

    if (lastReveal == 0 || lastReveal + slashRevealWindowTime < block.timestamp) {
        revealStartTime = block.timestamp;
    } else {
        revealStartTime = lastReveal + slashRevealWindowTime;
    }

    slashCommitments[account][hash] = revealStartTime;
    lastRevealStartTime[account] = revealStartTime;
}
```
The hash is based on a PK and a reward recipient address. Thus, it seems like an assumption is made that this hash would only ever be used from the legitimate address as he is the one who benefits from having his own reward recipient address. However, any other slasher can simply spam the function a lot using someone else's hash and cause the reveal time for that slash to be very far in the future, thus disallow that slasher from getting the rewards he is entitled to. Then, he can be the one who actually gets these rewards.

**Impact:** Any slasher can significantly increase another one's reveal delays

**Recommended Mitigation:** Consider adding another key to `slashCommitments` which holds the address who commits (`msg.sender` during `slashCommit` call).

**StatusL2:** Fixed in [f15f5e9](https://github.com/status-im/status-network-monorepo/commit/f15f5e9997243a1991c4dadc98f790bfe57ae100).

**Cyfrin:** Verified.

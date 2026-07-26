---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-02-cyfrin-evo-soulboundtoken-v2-0-0-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-06-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md
tags:
- firm:cyfrin
- report:2025-06-02-cyfrin-evo-soulboundtoken-v2-0
title: Users who are removed from the blacklist have to pay again for their NFT
vuln_class: []
---

# Users who are removed from the blacklist have to pay again for their NFT

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md)_

---

**Description:** When a user is added to the blacklist, the NFT which they already paid for is burned:
```solidity
function _addToBlacklist(address account) internal {
    // *snip: code not relevant *//

    if (balanceOf(account) > 0) {
        uint256 tokenId = tokenOfOwnerByIndex(account, 0); // Get first token
        _burn(tokenId); // Burn the token
    }
}
```

But when they are removed from the blacklist, they do not receive a free NFT to make up for their previously burned one, nor is there any flag set that would enable them to mind their NFT again but without paying a fee:
```solidity
function _removeFromBlacklist(address account) internal {
    if (!s_blacklist[account]) revert SoulBoundToken__NotBlacklisted(account);

    s_blacklist[account] = false;
    emit RemovedFromBlacklist(account);
}
```

**Impact:** A user who bought an NFT, then was blacklisted, then removed from the blacklist will have to pay twice to get the NFT.

**Recommended Mitigation:** This doesn't seem fair; if a user had an NFT burned when they were blacklisted, they should receive a free NFT back if later removed from the blacklist.

**Evo:**
Acknowledged; in the unlikely case a user is blacklisted due to admin error then subsequently removed from the blacklist, the DAO will compensate the user via a community vote.

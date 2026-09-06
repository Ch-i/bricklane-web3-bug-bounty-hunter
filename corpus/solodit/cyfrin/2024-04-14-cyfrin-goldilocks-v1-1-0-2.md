---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-0-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-04-14T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
tags:
- firm:cyfrin
- report:2024-04-14-cyfrin-goldilocks-v1-1
title: Users can extend an expired boost using invalidated NFTs.
vuln_class: []
---

# Users can extend an expired boost using invalidated NFTs.

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-14-cyfrin-goldilocks-v1.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md)_

---

**Severity:** High

**Description:** In `Goldilend.sol#L251`, a user can extend a boost with invalidated NFTs.
- The user has created a boost with a valid NFT.
- After that, the NFT was invalidated using `adjustBoosts()`.
- After the original boost is expired, the user can just call `boost()` with empty arrays, and the boost will be extended again with the original magnitude.

```solidity
  function _buildBoost(
    address[] calldata partnerNFTs,
    uint256[] calldata partnerNFTIds
  ) internal returns (Boost memory newUserBoost) {
    uint256 magnitude;
    Boost storage userBoost = boosts[msg.sender];
    if(userBoost.expiry == 0) {
...
    }
    else {
      address[] storage nfts = userBoost.partnerNFTs;
      uint256[] storage ids = userBoost.partnerNFTIds;
      magnitude = userBoost.boostMagnitude; //@audit use old magnitude without checking
      for (uint256 i = 0; i < partnerNFTs.length; i++) {
        magnitude += partnerNFTBoosts[partnerNFTs[i]];
        nfts.push(partnerNFTs[i]);
        ids.push(partnerNFTIds[i]);
      }
      newUserBoost = Boost({
        partnerNFTs: nfts,
        partnerNFTIds: ids,
        expiry: block.timestamp + boostLockDuration,
        boostMagnitude: magnitude
      });
    }
  }
```

**Impact:** Malicious users can use invalidated NFTs to extend their boosts forever.

**Recommended Mitigation:** Whenever users extend their boosts, their NFTs should be evaluated again.

**Client:** Fixed in [PR #3](https://github.com/0xgeeb/goldilocks-core/pull/3)

**Cyfrin:** Verified.

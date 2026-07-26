---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-19-cyfrin-linea-spingame-v2-0-1-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-03-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-19-cyfrin-linea-spingame-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-19-cyfrin-linea-spingame-v2-0
title: Users can select higher-value NFTs by delaying prize claims
vuln_class: []
---

# Users can select higher-value NFTs by delaying prize claims

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-19-cyfrin-linea-spingame-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-19-cyfrin-linea-spingame-v2.0.md)_

---

**Description:** When a user wins, the contract only tracks that they have won a specific `prizeID` in [`Spin::_fulfillRandomness`](https://github.com/Consensys/linea-hub/blob/295344925ec4321265f7cbac174fcf903b529a4e/contracts/src/Spin.sol#L576-L592):

```solidity
    if (winningThreshold < cumulativeProbability) {
        selectedPrizeId = localPrizeIds[i];

        // ...
        break;
    }
}

userToPrizesWon[user][selectedPrizeId] += 1;
```

However, when a user claims their prize, if the prize is an NFT, the contract simply assigns them the last available NFT in the list in [`Spin::_transferPrize`](https://github.com/Consensys/linea-hub/blob/295344925ec4321265f7cbac174fcf903b529a4e/contracts/src/Spin.sol#L366-L368):

```solidity
uint256 tokenId = prize.availableERC721Ids[
    prize.availableERC721Ids.length - 1
];
```

Since NFTs are non-fungible, each `tokenId` represents a unique item, meaning that a user who wins can wait to claim their prize until the highest-value NFT remains in the collection. This allows them to strategically claim the best available token, potentially at the expense of users who claim their prizes immediately.

**Impact:** Users could delay claiming to secure a more valuable NFT from a collection, while other users who claim immediately may unknowingly receive lower-value tokens. This could create an unfair advantage for informed users who understand the mechanics of prize allocation.

**Recommended Mitigation:** There is no perfect solution, as all potential fixes come with trade-offs. One approach would be to assign a specific NFT at the time of winning in `_fulfillRandomness`. However, this would require tracking both which NFTs each user has won and which remain available, significantly increasing state complexity and gas costs.

Instead, the protocol should be aware of this issue and ensure that NFTs within each prize category have similar values. If a collection includes NFTs with widely varying values, they should be added as separate prizes, ensuring fairer distribution and preventing users from gaming the system.

**Linea:** Acknowledged. Higher value NFTs should be added as separate prizes.

**Cyfrin:** Acknowledged.

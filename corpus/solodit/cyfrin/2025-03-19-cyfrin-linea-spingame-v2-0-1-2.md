---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-19-cyfrin-linea-spingame-v2-0-1-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-03-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-19-cyfrin-linea-spingame-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-19-cyfrin-linea-spingame-v2-0
title: Probability overflow can bypass `MaxProbabilityExceeded` check
vuln_class: []
---

# Probability overflow can bypass `MaxProbabilityExceeded` check

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-19-cyfrin-linea-spingame-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-19-cyfrin-linea-spingame-v2.0.md)_

---

**Description:** When adding new prizes, the contract includes a check to ensure that the total probability does not exceed 100% in [`Spin::_addPrizes#L511-L513`](https://github.com/Consensys/linea-hub/blob/295344925ec4321265f7cbac174fcf903b529a4e/contracts/src/Spin.sol#L511-L513):

```solidity
if (totalProbabilities > BASE_POINT) {
    revert MaxProbabilityExceeded(totalProbabilities);
}
```

However, this check can be bypassed due to how `totalProbabilities` is calculated. The accumulation of probabilities happens in `unchecked` blocks at the following locations:

- First accumulation of individual probability values, [`Spin::_addPrizes#L503-L505`](https://github.com/Consensys/linea-hub/blob/295344925ec4321265f7cbac174fcf903b529a4e/contracts/src/Spin.sol#L503-L505):

  ```solidity
  unchecked {
      totalProbIncrease += probability;
  }
  ```

- Final update of `totalProbabilities`, [`Spin::_addPrizes#L508-L510`](https://github.com/Consensys/linea-hub/blob/295344925ec4321265f7cbac174fcf903b529a4e/contracts/src/Spin.sol#L508-L510):

  ```solidity
  unchecked {
      totalProbabilities += totalProbIncrease;
  }
  ```

Because both updates occur within `unchecked` blocks, a very large probability value can overflow, effectively bypassing the `MaxProbabilityExceeded` check. This could allow `totalProbabilities` to wrap around and appear valid, even if it exceeds `BASE_POINT`.

**Impact:** Although this function can only be called by trusted users (e.g., the `CONTROLLER` or `DEFAULT_ADMIN` role), a mistake or a compromised account could still trigger this issue by adding an excessively large probability value. This would cause an overflow, allowing the ``MaxProbabilityExceeded check to be bypassed and potentially breaking the integrity of the game by distorting the prize distribution.

**Proof of Concept:** Add the following test to `Spin.t.sol`:
```solidity
function testUpdateWithMoreThanMaxProba() external {
    MockERC721 nft = new MockERC721("Test NFT", "TNFT");
    nft.mint(address(spinGame), 10);
    nft.mint(address(spinGame), 21);

    ISpinGame.Prize[] memory prizesToUpdate = new ISpinGame.Prize[](2);
    uint256[] memory empty = new uint256[](0);

    uint256[] memory nftAvailable = new uint256[](2);
    nftAvailable[0] = 10;
    nftAvailable[1] = 21;

    prizesToUpdate[0] = ISpinGame.Prize({
        tokenAddress: address(nft),
        amount: 0,
        lotAmount: 2,
        probability: type(uint64).max - 1,
        availableERC721Ids: nftAvailable
    });

    prizesToUpdate[1] = ISpinGame.Prize({
        tokenAddress: address(0),
        amount: 1e18,
        lotAmount: 2,
        probability: 2,
        availableERC721Ids: empty
    });

    vm.prank(admin);
    spinGame.updatePrizes(prizesToUpdate);

    assertEq(spinGame.getPrize(1).probability, type(uint64).max - 1);
}
```

**Recommended Mitigation:** Consider removing the `unchecked` blocks in both calculations.

**Linea:** Fixed in commit [`e840e2f`](https://github.com/Consensys/linea-hub/commit/e840e2f04dca6006ac7b5782765c58e7a6869603)

**Cyfrin:** Verified.

\clearpage

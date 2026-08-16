---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-30-cyfrin-linea-spingame-v2-v2-1-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-06-30T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-30-cyfrin-linea-spingame-v2-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-30-cyfrin-linea-spingame-v2-v2-1
title: Lack of validation when updating prizes can lead to `lotAmount` underflow when
  randomness is fulfilled
vuln_class: []
---

# Lack of validation when updating prizes can lead to `lotAmount` underflow when randomness is fulfilled

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-30-cyfrin-linea-spingame-v2-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-30-cyfrin-linea-spingame-v2-v2.1.md)_

---

**Description:** In [`SpinGame::_fulfillRandomness`](https://github.com/Consensys/linea-hub/blob/0af327319636960e9683897c5935aa1a78d1ded5/contracts/src/Spin.sol#L595-L603), there's an `unchecked` block that decrements `prize.lotAmount` without validating its current value:

```solidity
/// Should never underflow due to earlier check.
unchecked {
    prize.lotAmount -= 1;
}

if (prize.lotAmount == 0) {
    totalProbabilities -= prizeProbability;
    prize.probability = 0;
}
```

However, the comment claiming that the underflow is prevented by "an earlier check" is outdated as the check was removed in commit [`db6ae3d`](https://github.com/Consensys/linea-hub/commit/db6ae3d7a68497ac1077297ab0a16b9c13bd9a73#diff-ca99e3568f81fcb74ee275bb22d15e8216159decd2a4cc2e7c4572f639bb27c3R536), making the assumption incorrect. As a result, if a prize is added with a `lotAmount` of 0, the unchecked decrement will underflow to `type(uint32).max`.

**Impact:** This underflow results in the prize appearing to have an extremely large `lotAmount`, allowing users to repeatedly win and claim that prize well beyond the intended quantity. While this requires a misconfiguration by an admin (e.g. setting `lotAmount = 0`), such errors are plausible in practice and could go unnoticed.


**Proof of Concept:** The following test demonstrates the underflow in `lotAmount` when a prize is registered with `lotAmount = 0`:
```solidity
function testFulfillRandomnessWith0LotAmount() external {
    MockERC20 token = new MockERC20("Test Token", "TST");
    ISpinGame.Prize[] memory prizesToUpdate = new ISpinGame.Prize[](1);
    uint256[] memory empty = new uint256[](0);

    prizesToUpdate[0] = ISpinGame.Prize({
        tokenAddress: address(token),
        amount: 500 * 1e18,
        lotAmount: 0,
        probability: 1e8,
        availableERC721Ids: empty
    });

    vm.prank(controller);
    spinGame.updatePrizes(prizesToUpdate);

    uint64 nonce = 1;
    uint64 expirationTimestamp = uint64(block.timestamp + 1);
    uint64 boost = 1e8;

    ISpinGame.ParticipationRequest memory request = ISpinGame.ParticipationRequest({
        user: user,
        expirationTimestamp: expirationTimestamp,
        nonce: nonce,
        boost: boost
    });

    bytes32 messageHash = spinGame.hashParticipationExt(request);
    (uint8 v, bytes32 r, bytes32 s) = vm.sign(signer, messageHash);
    ISpinGame.Signature memory signature = ISpinGame.Signature(r, s, v);

    assertFalse(spinGame.nonces(user, nonce));

    vm.prank(user);
    uint256 requestId = spinGame.participate(nonce, expirationTimestamp, boost, signature);
    assertTrue(spinGame.nonces(user, nonce));

    bytes memory extraData = new bytes(0);
    bytes memory data = abi.encode(requestId, extraData);

    uint256 round = 15608646;
    bytes memory dataWithRound = abi.encode(round, data);

    vm.prank(vrfOperator);
    spinGame.fulfillRandomness(2, dataWithRound);

    uint32[] memory prizeIds = new uint32[](1);
    prizeIds[0] = 0;
    uint256[] memory amounts = spinGame.getUserPrizesWon(user, prizeIds);
    assertEq(amounts[0], 1);
    assertEq(spinGame.hasWonPrize(user, 0), true);

    ISpinGame.Prize memory prize = spinGame.getPrize(0);
    assertEq(prize.lotAmount,type(uint32).max);
}
```

**Recommended Mitigation:** To prevent this underflow, validate that `lotAmount > 0` when registering new prizes in `_addPrizes`:

```diff
    uint32 lotAmount = _prizes[i].lotAmount;

+   if (lotAmount == 0) {
+       revert InvalidLotAmount();
+   }

    if (prizeAmount == 0) {
        if (erc721IdsLen != lotAmount) {
            revert MismatchERC721PrizeAmount(erc721IdsLen, lotAmount);
        }
    } else {
        if (erc721IdsLen != 0) {
            revert ERC20PrizeWrongParam();
        }
    }
```

This ensures that any prize expected to be distributed has a non-zero quantity, eliminating the possibility of underflow during fulfillment.

**Linea:** Fixed in commit [`02d6d57`](https://github.com/Consensys/linea-hub/pull/551/commits/02d6d576cced6a6926ae12e2f187d8ef2fee771e)

**Cyfrin:** Verified. `lotAmount` no verified to be non-zero when a new prize is added.

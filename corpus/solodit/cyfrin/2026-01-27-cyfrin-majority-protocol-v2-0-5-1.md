---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-5-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: Cache identical storage reads and only write to storage once
vuln_class: []
---

# Cache identical storage reads and only write to storage once

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** Reading from storage is expensive; cache identical storage reads to prevent re-reading identical values from storage. Writing to storage is also expensive; increment cached values then write to storage only once when processing is complete:
* `DepositManager.sol`:
```solidity
// cache `pool.token` in `sponsorGame` saves 1 storage read
135:        emit GameSponsored(gameId, msg.sender, pool.token, amount);
136:        SafeERC20.safeTransferFrom(IERC20(pool.token), msg.sender, address(this), amount);

// cache `gamePools[gameId].token` in `_claimReferralReward` saves 1 storage read
142:        SafeERC20.safeTransfer(IERC20(gamePools[gameId].token), msg.sender, referralReward);
143:        emit ReferralRewardClaimed(gameId, msg.sender, gamePools[gameId].token, referralReward);

// cache `pool.token`, `pool.totalCollectedAmount * pool.creatorFee / BASIS_POINTS`,
// `pool.totalCollectedAmount * pool.protocolFee / BASIS_POINTS` in `_distributeFees`
// to save 6 storage reads
152:            pool.token,
154:            pool.totalCollectedAmount * pool.creatorFee / BASIS_POINTS,
156:            pool.totalCollectedAmount * pool.protocolFee / BASIS_POINTS
158:        SafeERC20.safeTransfer(IERC20(pool.token), creator, pool.totalCollectedAmount * pool.creatorFee / BASIS_POINTS);
160:           IERC20(pool.token), protocolTreasury, pool.totalCollectedAmount * pool.protocolFee / BASIS_POINTS

// cache `sponsorAmounts[sponsor][gameId]` before the `require` check
// in `_refundSponsorFunds` saves 1 storage read, caching `pool.token` afterwards
// also saves 1 storage read
165:        require(sponsorAmounts[sponsor][gameId] > 0, AlreadyRefunded(sponsor, gameId));
167:        uint256 amount = sponsorAmounts[sponsor][gameId];
170:        emit RefundSponsorFunds(gameId, sponsor, pool.token, amount);
171:        SafeERC20.safeTransfer(IERC20(pool.token), sponsor, amount);

// cache `pool.ticketPrice` in `_refundEntryFee` saves 2 storage reads
183:        require(pool.totalCollectedAmount >= pool.ticketPrice, NotEnoughFunds(pool.token, pool.totalCollectedAmount));
186:        SafeERC20.safeTransfer(IERC20(pool.token), player, pool.ticketPrice);
187:        pool.totalCollectedAmount -= pool.ticketPrice;

// cache `pool.token`, `pool.ticketPrice` in `_payEntryFee` saves 7 storage reads
193:            IERC20(pool.token).balanceOf(player) >= pool.ticketPrice,
196:                token: pool.token,
197:                balance: IERC20(pool.token).balanceOf(player),
198:                required: pool.ticketPrice
201:        SafeERC20.safeTransferFrom(IERC20(pool.token), player, address(this), pool.ticketPrice);
202:        pool.totalCollectedAmount += pool.ticketPrice;
203:        referralRewards[gameId][Registry(registry).referrers(player)] += pool.ticketPrice * REFERRER_FEE;
```

* `QuestionManager.sol`:
```solidity
// cache `nextQuestionId` to save 3 storage reads per loop iteration in `_commitQuestions`
// writing to storage is also expensive so ideally only want to write to storage once when updating
// nextQuestionId. Do it like this to be much more efficient:

// cache prior to loop
uint256 nextQuestionIdCache = nextQuestionId;

for (uint256 i; i < _questionHashes.length; i++) {
    require(_questionHashes[i] != bytes32(0), InvalidQuestionHash(_gameId, i));

    // use cached value to save identical storage reads
    require(
        questionCommitment[nextQuestionIdCache].promptHash == bytes32(0),
        QuestionAlreadyCommitted(_gameId, nextQuestionIdCache)
    );
    gameQuestions[_gameId].push(nextQuestionIdCache);
    questionCommitment[nextQuestionIdCache] =
        PromptInitData({promptHash: _questionHashes[i], promptStrategy: _promptStrategies[i]});
    emit QuestionCommitted(_gameId, nextQuestionIdCache, _questionHashes[i], _promptStrategies[i]);

    // increment cache at end of each loop iteration
    nextQuestionIdCache++;
}

// once loop finished, write to storage once
nextQuestionId = nextQuestionIdCache;
```

* `SessionManager.sol`:
```solidity
// cache `game.startTime` in `startAndRevealGameQuestion` saves ` storage read
402:        require(block.timestamp >= game.startTime, GameHasNotStartedYet(game.startTime, block.timestamp));
404:            block.timestamp <= game.startTime + revealGracePeriod,

// cache `questions.length` in `endGame` saves `questions.length - 1` storage reads
438:        for (uint256 i = 0; i < questions.length; i++) {

// cache `games[_gameId].state` in `cancelGame`, cancelGameIfCreatorMissing` saves 1 storage read
452:            games[_gameId].state != SessionState.Cancelled,
456:            games[_gameId].state != SessionState.Concluded,
465:            games[_gameId].state != SessionState.Cancelled,
469:            games[_gameId].state != SessionState.Concluded,
```

* `DefaultSession.sol`:
```solidity
// cache `assertion.winners.length` in `recordResults`
172:        for (uint256 i = 0; i < assertion.winners.length; ++i) {

// cache `assertion.totalXPs[i], assertion.totalTimes[i]` in `recordResults`
// also at L180 instead of `assertion.sessionId` can use input `sessionId` as they
// were asserted equal at L164
177:                    questionIds[j], winner, assertion.totalXPs[i], assertion.totalTimes[i]
181:                SessionResult({placement: i + 1, xp: assertion.totalXPs[i], time: assertion.totalTimes[i]});
```

* `MajorityChoicePrompt.sol`:
```solidity
// cache `revealedAt[_questionId]` in `commitReaction`
// same thing applies in `TriviaChoicePrompt` & `SPBinaryPrompt` `commitReaction` function
106:        require(revealedAt[_questionId] != 0, QuestionNotRevealed(_questionId));
112:            revealedAt[_questionId] + revealedQuestions[_questionId].reactionDeadline > block.timestamp,
```

**Majestic Games:**
Fixed in commit [4e56c11](https://github.com/Engage-Protocol/engage-protocol/commit/4e56c1123865865224b24583a6abadb4348fcc69).

**Cyfrin:** Verified.

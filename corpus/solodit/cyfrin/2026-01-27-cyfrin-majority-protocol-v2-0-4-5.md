---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-4-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: Rename all `sessionId` to `gameId` or vice versa for consistency
vuln_class: []
---

# Rename all `sessionId` to `gameId` or vice versa for consistency

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** `sessionId` appears to be used interchangeably with `gameId`; for consistency it would be best to rename all `sessionId` to `gameId` (or vice versa) where the same meaning is intended:
```solidity
session/DefaultSession.sol
44:    error SessionIdMismatch(uint256 sessionId, uint256 assertionSessionId);
137:     * @param sessionId The session ID
144:        uint256 sessionId,
150:        require(SessionManager(sessionManager).getSessionState(sessionId) == SessionState.Ended, GameNotEnded());
152:            sessionId, resultCid, resolutionGitRepoAtCommitHash, proposedWinners, totalXPs, totalTimes, msg.sender
158:     * @param sessionId The session ID
161:    function recordResults(uint256 sessionId, bytes32 assertionId) public {
162:        require(SessionManager(sessionManager).getSessionState(sessionId) == SessionState.Ended, GameNotEnded());
164:            sessionId == assertions[assertionId].sessionId,
165:            SessionIdMismatch(sessionId, assertions[assertionId].sessionId)
168:        require(winners[sessionId].length == 0, WinnersAlreadyRecorded(sessionId));
170:        uint256[] memory questionIds = SessionManager(sessionManager).getQuestionsForGame(sessionId);
180:            userResult[assertion.sessionId][winner] =
184:        winners[sessionId] = assertion.winners;
195:                dataAssertion.sessionId,
201:            recordResults(assertions[assertionId].sessionId, assertionId);

session/ISessionStrategy.sol
24:    error WinnersAlreadyRecorded(uint256 sessionId);
57:     * @param sessionId The session ID
64:        uint256 sessionId,
73:     * @param sessionId The session ID
76:    function recordResults(uint256 sessionId, bytes32 assertionId) external;

reward/IRewardStrategy.sol
13:    error NotCreator(uint256 sessionId, address sender);
14:    error AlreadySet(uint256 sessionId);
15:    error NotCreated(uint256 sessionId);

offchain/uma/SessionResultAsserter.sol
20:        uint256 sessionId;
33:        uint256 indexed sessionId,
41:        uint256 indexed sessionId,
62:        uint256 sessionId,
79:                "sessionId asserted: ",
80:                sessionId,
107:            sessionId, resultCid, resolutionGitRepoAtCommitHash, asserter, false, winners, totalXPs, totalTimes
109:        emit DataAsserted(sessionId, resultCid, resolutionGitRepoAtCommitHash, asserter, assertionId);

reward/FixedRanksReward.sol
19:    event RankedRewardsUpdated(uint256 indexed sessionId, uint256[] rankedRewards);
21:    error RankedRewardsNotSet(uint256 sessionId);
22:    error InvalidRanks(uint256 sessionId, uint256 numRanks);
23:    error InvalidTotalPoints(uint256 sessionId, uint256 numPoints);
29:    mapping(uint256 sessionId => uint256[]) public rankedRewards;
47:     * @param sessionId The ID of the game
50:    function setRankedRewards(uint256 sessionId, uint256[] calldata _rankedRewards) external {
51:        require(sessionManager.getSessionState(sessionId) == SessionState.Created, NotCreated(sessionId));
52:        require(sessionManager.getCreator(sessionId) == msg.sender, NotCreator(sessionId, msg.sender));
53:        require(rankedRewards[sessionId].length == 0, AlreadySet(sessionId));
54:        require(_rankedRewards.length > 0, InvalidRanks(sessionId, _rankedRewards.length));
55:        require(_rankedRewards.length <= 20, InvalidRanks(sessionId, _rankedRewards.length));
62:        require(totalPoints == BASIS_POINTS, InvalidTotalPoints(sessionId, totalPoints));
64:        rankedRewards[sessionId] = _rankedRewards;
65:        emit RankedRewardsUpdated(sessionId, _rankedRewards);
69:    function getRewards(uint256 sessionId, address[] calldata winners, uint256 prizePool)
74:        require(rankedRewards[sessionId].length > 0, RankedRewardsNotSet(sessionId));
77:            rewards[i] = prizePool * rankedRewards[sessionId][i] / BASIS_POINTS;
82:    function getReward(uint256 sessionId, address[] calldata, uint256 position, uint256 prizePool)
87:        require(rankedRewards[sessionId].length > 0, RankedRewardsNotSet(sessionId));
88:        reward = prizePool * rankedRewards[sessionId][position] / BASIS_POINTS;

reward/ProportionalToXPReward.sol
19:    event NumberOfWinnersUpdated(uint256 indexed sessionId, uint256 numberOfWinners);
21:    error NumberOfWinnersMismatch(uint256 sessionId, uint256 numberOfWinners);
28:    mapping(uint256 sessionId => uint256 numberOfWinners) public numberOfWinners;
35:    function getRewards(uint256 sessionId, address[] calldata winners, uint256 prizePool)
40:        require(numberOfWinners[sessionId] == winners.length, NumberOfWinnersMismatch(sessionId, winners.length));
41:        ISessionStrategy sessionStrategy = ISessionStrategy(sessionManager.getSessionStrategy(sessionId));
45:            (, uint256 xp,) = sessionStrategy.userResult(sessionId, winners[i]);
56:    function getReward(uint256 sessionId, address[] calldata winners, uint256 position, uint256 prizePool)
61:        require(numberOfWinners[sessionId] == winners.length, NumberOfWinnersMismatch(sessionId, winners.length));
62:        ISessionStrategy sessionStrategy = ISessionStrategy(sessionManager.getSessionStrategy(sessionId));
66:            (, uint256 xp,) = sessionStrategy.userResult(sessionId, winners[i]);
75:    function setNumberOfWinners(uint256 sessionId, uint256 _numberOfWinners) external {
76:        require(sessionManager.getSessionState(sessionId) == SessionState.Created, NotCreated(sessionId));
77:        require(sessionManager.getCreator(sessionId) == msg.sender, NotCreator(sessionId, msg.sender));
78:        require(numberOfWinners[sessionId] == 0, AlreadySet(sessionId));
79:        numberOfWinners[sessionId] = _numberOfWinners;
80:        emit NumberOfWinnersUpdated(sessionId, _numberOfWinners);
```

**Majority Games:**
Fixed in commit [75663d1](https://github.com/Engage-Protocol/engage-protocol/commit/75663d17c2a514eac4ccc7c01bb2d780ed344ab3) - everything is now `sessionId`.

**Cyfrin:** Verified.

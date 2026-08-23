---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-3-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: Excessive amount `maximumContestants` could make games to revert in `DefaultSession::recordResults`
  due to out of gas
vuln_class: []
---

# Excessive amount `maximumContestants` could make games to revert in `DefaultSession::recordResults` due to out of gas

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** `SessionManager::maximumContestants` is initially set to 1 million so potentially a large number of contestants can join each game:
```solidity
/**
 * @notice Maximum number of contestants allowed in a game
 */
 uint256 public maximumContestants = 1_000_000;
```

`DefaultSession::recordResults` iterates over all the winners to record the result for each question in the respective strategies:
```solidity
 function recordResults(uint256 sessionId, bytes32 assertionId) public {
     ...
        for (uint256 i = 0; i < assertion.winners.length; ++i) { <------
            address winner = assertion.winners[i]; //@audit how many winners could be?
            for (uint256 j = 0; j < questionIds.length; ++j) {
                (, address promptStrategy) = SessionManager(sessionManager).questionCommitment(questionIds[j]);
                IPromptStrategy(promptStrategy).recordResult(
                    questionIds[j], winner, assertion.totalXPs[i], assertion.totalTimes[i]
                );
            }
         ...
    }
```

If there are many winners this loop iteration could revert due to out-of-gas.

**Impact:** Games may not finish due to out of gas.

**Proof of Concept:** Taking in consideration that the block gas limit in base is around 30M and if we call ` forge test --mt test_RecordResults_Success --gas-report `  we could see that the `assertionResolvedCallback` is costing an avg 280587 for just two winners if we divide 30M /  280587  we get approximately 100 winner maximum.

**Assumptions:**
Block gas limit: 30,000,000 gas
Function overhead: ~50,000 gas

**Average questions per game: 5-10 questions
Conservative Estimate (10 questions per game):**
Gas per winner: 25,000 + (7,600 × 10) = 101,000 gas
Available gas: 30,000,000 - 50,000 = 29,950,000 gas
Maximum winners: 29,950,000 ÷ 101,000 ≈ 296 winners

**Optimistic Estimate (5 questions per game):**
Gas per winner: 25,000 + (7,600 × 5) = 63,000 gas
Maximum winners: 29,950,000 ÷ 63,000 ≈ 475 winners

**Realistic Maximum: ~300-400 winners**

**Recommended Mitigation:** Consider set a realistic `maximumContestants` to approx. 1000 participants. Alternatively another approach is just keep the winners in the array and create another function where user can `recordResult` by chunks.

**Majority Games:**
Fixed in commit [a2e353e](https://github.com/Engage-Protocol/engage-protocol/commit/a2e353e664f7707d49a3ca9ca2bea792d731711c).

**Cyfrin:** Verified.

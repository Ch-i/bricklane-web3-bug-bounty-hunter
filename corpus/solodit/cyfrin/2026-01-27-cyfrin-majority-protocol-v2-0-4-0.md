---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-4-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: Use named mappings to explicitly denote the purpose of keys and values
vuln_class: []
---

# Use named mappings to explicitly denote the purpose of keys and values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** Use named mappings to explicitly denote the purpose of keys and values; the protocol does use named mappings in some places but not others:
```solidity
session/DefaultSession.sol
60:    mapping(uint256 gameId => uint256[]) public xpTiers;

QuestionManager.sol
39:    mapping(uint256 => uint256[]) public gameQuestions;
40:    mapping(uint256 => PromptInitData) public questionCommitment;

Registry.sol
29:    mapping(address => bool) public promptStrategies;
30:    mapping(address => bool) public sessionStrategies;
31:    mapping(address => bool) public rewardStrategies;
32:    mapping(address => bool) public paymentTokens;
33:    mapping(address => bool) public engageProtocols;

DepositManager.sol
72:    mapping(uint256 => mapping(address => bool)) public hasClaimed;
77:    mapping(uint256 => mapping(address => bool)) public hasRefunded;

SessionManager.sol
164:    mapping(uint256 => Game) public games;
174:    mapping(address => bool) public isVerificationApproved;
179:    mapping(address => uint256 timestamp) public liveness;

reward/FixedRanksReward.sol
29:    mapping(uint256 sessionId => uint256[]) public rankedRewards;

offchain/uma/SessionResultAsserter.sol
30:    mapping(bytes32 => Assertion) public assertions;
```

**Majority Games:**
Fixed in commit [130e0a3](https://github.com/Engage-Protocol/engage-protocol/commit/130e0a33b69cc7381a0eea12719f14156bcc3446) where we felt this added value.

**Cyfrin:** Verified.

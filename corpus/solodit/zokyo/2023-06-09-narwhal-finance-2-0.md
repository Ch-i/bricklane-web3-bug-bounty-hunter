---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-2-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Front-running Vulnerability in signUp Function
vuln_class: []
---

# Front-running Vulnerability in signUp Function

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Low

**Status**: Acknowledged

**Description**:

The signUp function in the given contract is vulnerable to front-running attacks. An attacker can monitor pending transactions in the mempool and observe a user attempting to sign up with a specific referral. The attacker can then send a transaction with a higher gas price to register with the same referral before the user's transaction gets processed. This may result in the attacker benefiting from the referral rewards that were intended for the user.

**Proof**:

User A initiates a transaction to call the signUp function with a specific referral address (Referrer B).
Attacker C observes the pending transaction in the mempool.
Attacker C sends a transaction calling the signUp function with the same referral address (Referrer B) and sets a higher gas price.
Due to the higher gas price, Attacker C's transaction gets processed before User A's transaction.
Attacker C is now registered under Referrer B, potentially affecting the rewards intended for User A.

**Recommendation** : 

Implement a commit-reveal scheme to prevent front-running attacks on the signUp function. This solution involves two steps: a commit phase where users submit a hashed version of their referral information, and a reveal phase where users later reveal their referral information. By concealing the referral information during the commit phase, the attacker cannot observe the pending transactions and exploit the front-running vulnerability.

**Fix** : The fix requires two steps for signup and the Recommendation increases the complexity of the contract while there is no serious impact on funds with this vulnerability acknowledged and no change by the dev team

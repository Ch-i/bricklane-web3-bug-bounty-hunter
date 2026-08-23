---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-24-narwhal-finance-1-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2024-01-24-narwhal-finance
title: Improper Implementation of Whitelisting in Private Transfer Mode
vuln_class: []
---

# Improper Implementation of Whitelisting in Private Transfer Mode

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-01-24-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal%20Finance.md)_

---

**Severity**: Medium

**Status** : Resolved 

**Description**:

The `BaseToken` contract contains a feature known as "Private Transfer Mode," intended to restrict token transfers exclusively to whitelisted addresses (controlled via `isRecipientAllowed`). However, the current implementation of this feature has a critical vulnerability. The contract logic allows a transaction if either the sender or the recipient is whitelisted, rather than requiring both parties to be on the whitelist. This loophole enables non-whitelisted addresses to receive tokens through a whitelisted intermediary.
**Scenario:**
Contract State: The contract is set to "Private Transfer Mode."
Initial Transfer: A whitelisted address (whitelistedUser) receives tokens from an allowed sender (e.g., the contract owner).
Secondary Transfer: The whitelistedUser then transfers these tokens to a non-whitelisted address (nonWhitelistedUser).
Result: Despite nonWhitelistedUser not being on the whitelist, they successfully receive tokens, effectively bypassing the whitelisting mechanism.
Implication:
This flaw permits unauthorized transfer of tokens to non-whitelisted addresses, undermining the security and control intended by the private transfer mode. This could lead to unauthorized token circulation, potentially disrupting the token economy and compromising the integrity of the contract.

**Recommendation:**

To rectify this vulnerability, modify the _transfer function to enforce whitelisting checks for both the sender and the recipient in private transfer mode. This can be achieved by updating the conditional check to require both parties to be whitelisted

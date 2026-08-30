---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-05-24-struct-finance-1-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-05-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md
tags:
- firm:zokyo
- report:2023-05-24-struct-finance
title: Investors can lose funds due to delay in withdrawal
vuln_class: []
---

# Investors can lose funds due to delay in withdrawal

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-05-24-Struct Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md)_

---

**Severity**: Low

**Status**: Acknowledged

**Description**

In contract FEYTraderJoeProduct, the rescueTokens() function allows an admin to withdraw all the tokens from the contract after 3 weeks from the tranche end time. Ideally, the investors should be first allowed to withdraw their funds first, or the contract can push the funds to them before calling rescueTokens(). Otherwise, it could result in a malicious admin withdrawing investor's tokens, in case the investors forget to withdraw their tokens after 3 weeks from the tranche end time.

**Recommendation**: 

It is advised to allow pushing of tokens to the investors or allow automatic withdrawal of tokens (such as with Chainlink keepers) to investors before rescue tokens. 

**Comments**:  The client acknowledged this issue, stating that they’ll be using multisig for Governance initially and that the 3 weeks time works as a cooldown period. They said that If the users forget to withdraw their funds, the Struct team will withdraw on their behalf and we will send it to the investor's address.

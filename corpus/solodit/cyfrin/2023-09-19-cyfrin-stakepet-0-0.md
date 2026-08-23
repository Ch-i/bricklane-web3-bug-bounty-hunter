---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-19-cyfrin-stakepet-0-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-09-19T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-stakepet.md
tags:
- firm:cyfrin
- report:2023-09-19-cyfrin-stakepet
title: Attackers can use a malicious yield token to steal funds from users
vuln_class: []
---

# Attackers can use a malicious yield token to steal funds from users

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-19-cyfrin-stakepet.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-stakepet.md)_

---

**Severity:** High

**Description:** According to the documentation and the current implementation, anyone can create a new StakePet contract and feed any address for the `YIELD_TOKEN`. As long as a contract implements `IYieldToken` interface, the contract will be created without problems.

An attacker can create a malicious `IYieldToken` implementation and use that to steal funds from users.
The StakePet contract relies on `YIELD_TOKEN.toToken()` and `YIELD_TOKEN.toValue()` in numerous places for accounting.
Consider a contract that has implemented different logic in `toToken()` and `toValue()` according to the owner's hidden flag.
The attacker is likely to let the malicious token contract work normally till the StakePet contract gets enough deposits.
Then they can switch the hidden flag as they needed to mess the accounting and take profit from it.
In the worst case, they can even manipulate the output of `IYieldToken::ERC20_TOKEN()` (maybe to freeze the user funds permanently).

**Impact:** User funds can be stolen or permanently locked.

**Recommended Mitigation:** Consider maintaining a whitelist of YIELD_TOKEN and allow creation of StakePet for only allowed yield tokens.

**Client:** Fixed in commit [308672e](https://github.com/Ranama/StakePet/commit/308672e914651ca2300f2b585d91f16764994bf7).

**Cyfrin:** Verified.

---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-01-02-onchain-trade-1-8
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-01-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-01-02-Onchain%20Trade.md
tags:
- firm:zokyo
- report:2023-01-02-onchain-trade
title: Argument might be risky
vuln_class: []
---

# Argument might be risky

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-01-02-Onchain Trade.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-01-02-Onchain%20Trade.md)_

---

**Severity**: Low

**Status**: Unresolved

**Description**

In contract VariableBorrow.sol - in methods borrow and repay the argument to mostly referring to msg.sender adds a dimension that can be exploited if things are not perfectly implemented in Router contract. The case in which the to is not msg.sender exists if router = msg.sender. But implementation of the router contract is not the concern of this audit's scope. If the router is exploited by an attacker to bypass the require check, severe consequences might take place that will lead to attackers exploiting others investors' collateral. In this contract presumably we have a securely implemented router, hence severity is low, but a simple coding refactor is recommended.

**Recommendation**:

It is a better coding practice and more secure to isolate those external methods in this discussed scenario. Create methods exposed for EOA callers without to for borrow and repay. Also, implement other methods restricted for the router callers that include the to address. As for the logic itself, implement it in internal methods to be invoked by the external methods, suggested saving gas of course.
**Note #1**:  No change done to address this.

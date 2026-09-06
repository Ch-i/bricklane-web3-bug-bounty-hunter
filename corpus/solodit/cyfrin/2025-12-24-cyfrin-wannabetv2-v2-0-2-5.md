---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-wannabetv2-v2-0-2-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-wannabetv2-v2-0
title: '`BetFactory::createBet` should revert in a number of scenarios to prevent
  abuse and ensure bets can be resolved'
vuln_class: []
---

# `BetFactory::createBet` should revert in a number of scenarios to prevent abuse and ensure bets can be resolved

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-wannabetv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md)_

---

**Description:** `BetFactory::createBet` should revert if:
* `treasury` is `address(0)`
* `msg.sender` and `taker` are the same
* `judge` is the same as `msg.sender` or `taker`

All of the scenarios represent errors either in initialization or bet creation so such transactions should revert. The first scenario where `treasury` is `address(0)` can prevent bet resolution for tokens which revert on transfer to `address(0)`, though cancelling will still work.

**WannaBet:** We allow maker/taker/judge to be same address as this is useful for testing and doesn't cause any technical issues.

In commits [5ec090f](https://github.com/gskril/wannabet-v2/commit/5ec090f3eb73899dc191bcdf81306e9ef2cb1ab1), [f1750a9](https://github.com/gskril/wannabet-v2/commit/f1750a975346b1472ef3306db31f6fc7bd2db3b5) implemented a fix such that if no treasury has been set any generated yield goes to the winner.

**Cyfrin:** Verified.

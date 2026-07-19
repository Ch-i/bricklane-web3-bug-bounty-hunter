---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-4-12
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: '`DefaultSession::assertResults` should verify input `sessionId` belongs to
  a game associated with its instance'
vuln_class: []
---

# `DefaultSession::assertResults` should verify input `sessionId` belongs to a game associated with its instance

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** `DefaultSession::assertResults` doesn't verify that the input `sessionId` belongs to a game associated with that instance of `DefaultSession`.

But different games can be associated with different instances of DefaultSession; see `SessionManager::getSessionStrategy`.

Consider this scenario:
* there are 2 games G1 and G2, each associated with a different instance of `DefaultSession` DS1 and DS2 but both DS1 and DS2 are associated with the same instance of `SessionManager`
* a good user calls `DS1::assertResults` with valid results to assert the results for G1
* a malicious user copies the exact inputs and calls `DS2::assertResults` with valid results to also assert the results for G1

In this state both DS1 and DS2 can have recorded winners for G1, even though DS2 isn't the correct strategy for G1.

This doesn't appear to be further abusable as `SessionManager::claimRewards` always gets the correct strategy instance and prevents winners from claiming more than once, but it doesn't seem like a good idea to allow this.

**Recommended Mitigation:** `DefaultSession::assertResults` should verify input `sessionId` belongs to a game associated with its instance.

**Majority Games:**
Fixed in commit [462c01a](https://github.com/Engage-Protocol/engage-protocol/commit/462c01a157f287014e14585bbb4008379a3126c2).

**Cyfrin:** Verified.

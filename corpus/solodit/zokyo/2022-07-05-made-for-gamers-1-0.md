---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-07-05-made-for-gamers-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2022-07-05T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-07-05-Made%20for%20gamers.md
tags:
- firm:zokyo
- report:2022-07-05-made-for-gamers
title: Iteration through all locks, including expired locks.
vuln_class: []
---

# Iteration through all locks, including expired locks.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2022-07-05-Made for gamers.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-07-05-Made%20for%20gamers.md)_

---

**Description**

Expo.sol: functions transfer(), send(), burn(), transferWithLock(). Functions iterate through all user's locks to verify that he doesn't transfer more than locked until some period of time. Iteration is performed through expired locks as well, performing unnecessary actions and increasing gas spendings. Also, in case there are a lot of locks for the user, iterating through all of them might consume more gas than allowed per transaction, preventing user from transferring his tokens. Issue is marked as medium, since only the owner can create locks for user.

**Recommendation**

Remove locks, which have expired after successful transfer.

**Re-audit comment**

Resolved

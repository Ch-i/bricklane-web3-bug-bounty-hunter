---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-kleidi-report-0-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-kleidi-report
title: '[L-01] Suggested Next Steps'
vuln_class: []
---

# [L-01] Suggested Next Steps

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Kleidi_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md)_

---

**Executive Summary**

The codebase is already very well tested and mature

Excluding known issues, such as performing MEV exposed operations, scenarios in which all parties turn malicious, or hypothetical scenarios in which Create2 hashing is broken, I wasn't able to identify any Medium nor High Severity risk in the codebase.

I believe the code can benefit by one more rounding of polish in terms of comments, and gas optimizations
You may also opt into simplifying all functions by making them perform a single operation per function

For example `addCalldataCheck` currently is used to:
- Set a wildcard check
- Set a non wildcard check
- Add more hashes to a non wildcard check

The code can benefit by being simplified by turning each of these operation into a separate function

However, none of these seem to cause any particular security concern

Given my broad experience with these type of codebases, my recommendation for next steps is to perform a Audit Contest or a Bug Bounty next as I believe it will be hard to find any specific researcher that will be able to find any flaws I missed, while in aggregate, some researchers may found something that would escape the average researcher

A few possible things I may have missed:
- Is there any parameter that result in a salt that is ambigous or could cause a clash?
- Is there any specific scenario in which one of the ambigous parameters can result in a effective front-run?

- Is there a way to use `SENTINEL` to cause reverts for recovery spells?

- Is there any way to pass a forged payload that would result in `calldata` vs `memory` being read differently, possibly sidestepping the various check put in place in the system?

I have extensively explored these ideas, however someone with a different background or tools may find something I missed

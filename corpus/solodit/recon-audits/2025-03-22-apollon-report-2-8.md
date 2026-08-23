---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-2-8
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[M-09] Users could opt to never use Pyth and always rely on the fallback feed
  due to lack of validation on certain functions'
vuln_class: []
---

# [M-09] Users could opt to never use Pyth and always rely on the fallback feed due to lack of validation on certain functions

_Section severity (from Solodit section header): Medium_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

The rationale for using Pyth and the Fallback oracle is logical:
Sometimes Pyth is unavailable

However, once Pyth becomes unavailable, people will have the option to constantly chose between Pyth and the fallback oracle

The fallback oracle is a push type oracle, meaning that it won't always be updated

This may create opportunity for arbitrage for:
- Redemptions
- Increasing Debts (as other account debts will not have their prices checked for staleness)

**Mitigation**

Overall you should rethink the FSM around how stale vs trusted prices could be used as the current implementation opens up for a lot of arbitrage and edge cases

You should consider changing fees based on the oracle you're using

An oracle deviation threshold + time to update are inherently +EV to arbitrageurs
You should consider changing fees based on which oracle is being used, where Pyth could have a lower fee and the fallback would most likely have to charge a higher fee

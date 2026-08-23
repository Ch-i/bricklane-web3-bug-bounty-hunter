---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-2-6
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
title: '[M-07] Ticking Interest Rate opens up to multi-block MEV - Directly Triggering
  Recovery Mode on the next block due to interest ticking'
vuln_class: []
---

# [M-07] Ticking Interest Rate opens up to multi-block MEV - Directly Triggering Recovery Mode on the next block due to interest ticking

_Section severity (from Solodit section header): Medium_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

Because Apollon charges an interest on borrowing, an attack can guarantee triggering Recovery Mode on the next block by simply borrowing up to the threshold

Triggering Recovery mode would then allow liquidating Troves that are below the TCR

This puts the attacker at risk as well, however with some setup the attack can be +EV, posing a close to unmitigatable risk to other Trove owners


**Mitigation**

Recovery Mode liquidations being too easily accessible is a big risk for users leveraging up

In order to avoid this you could opt-into:
1) Enforcing a Buffer for Opening Positions
- This unfortunately has the downside of allowing the triggering of Recovery Mode via multiple positions

2) Changing the mechanisms around how Recovery Mode works
- This requires extensive work, possible solutions can be: Increasing the fee as you open a Trove that brings the sytem towards recovery mode (Make the attack economically expensive)

3) Remove or Alter the logic for Recovery Mode by enforcing higher Liquidations
- This requires economic modelling

4) Introduce a Delay for Recovery Mode Liquidations like we did in eBTC
- This doesn't remove the risk but reduces it and makes the attack more expensive

---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-balancer-report-2-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Balancer_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-balancer-report
title: '[I-02] Address Checks'
vuln_class: []
---

# [I-02] Address Checks

_Section severity (from Solodit section header): Informational_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Balancer_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Balancer_Report.md)_

---

The addresses are correctly set

address public constant BALANCER_MULTISIG = 0x10A19e7eE7d7F8a52822f6817de8ea18204F2e4f
Confirmed, 6/11 multi 
https://etherscan.io/address/0x10A19e7eE7d7F8a52822f6817de8ea18204F2e4f#code

IERC20 public constant AURA = IERC20(0xC0c293ce456fF0ED870ADd98a0828Dd4d2903DBF); // OK
https://etherscan.io/address/0xC0c293ce456fF0ED870ADd98a0828Dd4d2903DBF#code

ILockAura public constant AURA_LOCKER = ILockAura(0x3Fa73f1E5d8A792C80F426fc8F84FBF7Ce9bBCAC); // OK
https://etherscan.io/address/0x3Fa73f1E5d8A792C80F426fc8F84FBF7Ce9bBCAC#code

---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-quill-finance-report-1-7
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-quill-finance-report
title: '[L-08] Incorrect Comment about blocks and adjustments'
vuln_class: []
---

# [L-08] Incorrect Comment about blocks and adjustments

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Quill_Finance_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md)_

---

**Impact**

Quill will reduce the min debt by a factor of 10

Bold had a potential risk when batch debt shares were rebased

The exploit was fixed and as far I was able to tell the system is safe from this exploit

Out of caution, as to maintain a similar risk profile as Liquity, it's best to 10x the `MIN_INTEREST_RATE_CHANGE_PERIOD` as to make it slower and more costly to rebase batches by spamming fees

Also the comment is incorrect since Scroll has faster (2/3 seconds) block times

https://github.com/subvisual/quill/blob/d4a5dcc168dfc315eef6a4c9c465a36c86ca0ddc/contracts/src/Dependencies/Constants.sol#L33-L34

```solidity
uint128 constant MIN_INTEREST_RATE_CHANGE_PERIOD = 120 seconds; // prevents more than one adjustment per ~10 blocks /// @audit this is MAINNET

```

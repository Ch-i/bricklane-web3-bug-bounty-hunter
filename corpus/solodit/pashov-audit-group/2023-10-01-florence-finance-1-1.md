---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-10-01-florence-finance-1-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-10-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-10-01-Florence%20Finance.md
tags:
- firm:pashov-audit-group
- report:2023-10-01-florence-finance
title: '[L-02] Upgradeability best practices are not followed'
vuln_class: []
---

# [L-02] Upgradeability best practices are not followed

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-10-01-Florence Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-10-01-Florence%20Finance.md)_

---

In `LoanVault` the storage layout has been changed in a non-upgradeability safe way. Between commit `616e9d4ba18eef293dc76fb95144bd11fb29549b` and the current HEAD of the `audit` branch it seems like the `fundingFee` storage variable has changed its place and also the whitelisting storage variables have been removed. This is quite dangerous as if a potential upgrade is done on the Ethereum contracts it can mess up the storage layout, potentially bricking the contract. This is highly unlikely to happen though as the protocol is using the OpenZeppelin's upgrades plugin which protects from this. Still, upgradeability best practices should always be applied - do not reorder storage variables and instead of removing old ones just deprecate them.

---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-06-25-cyber-finance-2-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-06-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-25-Cyber%20Finance.md
tags:
- firm:zokyo
- report:2024-06-25-cyber-finance
title: Owner Can Renounce Ownership While System is Paused
vuln_class: []
---

# Owner Can Renounce Ownership While System is Paused

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-06-25-Cyber Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-25-Cyber%20Finance.md)_

---

**Severity**: Low

**Status**: Acknowledged

**Description**

The `CyberFinance` contract inherits from `Ownable2Step` and includes Pausable functionality. However, the current implementation allows the owner to renounce ownership even while the system is paused. This can lead to a scenario where the contract is left in an unusable state and the funds could be locked there forever, as no one would have the authority to unpause the contract and resume normal operations.

**Recommendation**: 

Implement a check to prevent the owner from renouncing ownership while the contract is paused. This ensures that the system remains manageable and prevents it from being locked in a paused state indefinitely.

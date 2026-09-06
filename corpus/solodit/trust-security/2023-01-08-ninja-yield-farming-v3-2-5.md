---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-08-ninja-yield-farming-v3-2-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-01-08T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md
tags:
- firm:trust-security
- report:2023-01-08-ninja-yield-farming-v3
title: TRST-L-6 Strategy upgrade cooldown is set too low
vuln_class: []
---

# TRST-L-6 Strategy upgrade cooldown is set too low

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-01-08-Ninja Yield Farming v3.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md)_

---

**Description:** 
**UPGRADE_TIMELOCK** defines how long admin must wait before upgrading the contract. 
```solidity
      function _authorizeUpgrade(address) internal override {
            _atLeastRole(DEFAULT_ADMIN_ROLE);
      require(upgradeProposalTime + UPGRADE_TIMELOCK < block.timestamp);
          clearUpgradeCooldown();
             }
```
It is currently set to 1 hour, which is far too low in relation to its importance and funds at 
risk. We recommend a value of 24 hours at minimum to give the community a chance to 
respond to a malicious upgrade risk.

**Team response:**
Accepted, changed to 36 hours.

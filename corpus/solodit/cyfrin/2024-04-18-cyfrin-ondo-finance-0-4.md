---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-18-cyfrin-ondo-finance-0-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-04-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md
tags:
- firm:cyfrin
- report:2024-04-18-cyfrin-ondo-finance
title: '`OUSGInstantManager` redemptions will be bricked if BlackRock deploys a new
  `BUIDLRedeemer` contract and sunsets the existing one'
vuln_class: []
---

# `OUSGInstantManager` redemptions will be bricked if BlackRock deploys a new `BUIDLRedeemer` contract and sunsets the existing one

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-18-cyfrin-ondo-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md)_

---

**Description:** The `BUIDLRedeemer` contract is a very new contract; it is very possible that in the future a new version of the contract will be deployed and the current version will cease to function.

To future-proof `OUSGInstantManager` and ensure it will continue to function in this situation, remove the `immutable` keyword from the `buidlRedeemer` definition and add a setter function that allows it to be updated in the future.

**Ondo:**
If a new `BUIDLRedeemer` contract is deployed our plan is to deploy a new `OUSGInstantManager`. We prefer to make it harder for us to change the address of `buidlRedeemer` to ensure there is proper due diligence of any changes.

---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-01-02-onchain-trade-2-6
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-01-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-01-02-Onchain%20Trade.md
tags:
- firm:zokyo
- report:2023-01-02-onchain-trade
title: Save gas by rearranging variables in the struct Pool declaration
vuln_class: []
---

# Save gas by rearranging variables in the struct Pool declaration

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-01-02-Onchain Trade.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-01-02-Onchain%20Trade.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**


The structs used in the contract use storage slots in EVM. The arrangement of variables defined in the struct affects the storage slots required. All reads and writes to storage in Solidity are handled in 32-byte increments. Solidity tightly packs variables where possible, storing them within the same 32 bytes. The best use of storage available slots is possible by re-arranging the variables in the struct Pool such that multiple variables can be stored in the same storage slot.

**Recommendation**: 

Re-organize variables struct Pool declaration for efficient use of storage slot. Suggested declaration as below:

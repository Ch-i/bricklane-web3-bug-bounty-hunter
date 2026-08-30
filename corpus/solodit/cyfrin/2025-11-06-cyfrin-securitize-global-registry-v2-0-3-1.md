---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-06-cyfrin-securitize-global-registry-v2-0-3-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-11-06T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-06-cyfrin-securitize-global-registry-v2-0
title: In `StandardToken::updateNameAndSymbol` cache existing name and symbol then
  pass them to child functions
vuln_class: []
---

# In `StandardToken::updateNameAndSymbol` cache existing name and symbol then pass them to child functions

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-06-cyfrin-securitize-global-registry-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md)_

---

**Description:** `StandardToken::updateNameAndSymbol`:
* reads the existing `name` and `symbol`
* calls `CommonUtils.isEqualString` to compare existing to proposed new
* if different, calls `_updateName` and `_updateSymbol` which re-read the identical existing values from storage to emit the event

**Recommended Mitigation:** Since reading from storage is expensive, ideally `updateNameAndSymbol` would
* cache the existing `name` and `symbol`
* use the cached values for the call to `CommonUtils.isEqualString`
* pass the cached values to `_updateName` and `_updateSymbol` which can use them to emit the events

**Securitize:** Acknowledged.

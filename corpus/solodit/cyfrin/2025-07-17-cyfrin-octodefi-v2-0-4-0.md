---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-4-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-07-17T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-17-cyfrin-octodefi-v2-0
title: Unused cached value of `getStorageId(msg.sender, id)`
vuln_class: []
---

# Unused cached value of `getStorageId(msg.sender, id)`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-17-cyfrin-octodefi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md)_

---

**Description:** `createAutomation()` calls `getStorageId(msg.sender, id)` twice—once for `automationSID` and again when assigning `_newAutomation`. This duplicates the same keccak 256 computation and extra stack writes.

**Recommended Mitigation:** Store the first return value in a local variable and reuse it:

```solidity
bytes32 automationSID = getStorageId(msg.sender, id);
Automation storage _newAutomation = automations[automationSID];
```

This saves one `STATICCALL`/`KECCAK256` operation and a few stack ops per invocation.

**OctoDeFi:** Fixed in PR [\#21](https://github.com/octodefi/strategy-builder-plugin/pull/21).

**Cyfrin:** Verified. The cached value is now used.

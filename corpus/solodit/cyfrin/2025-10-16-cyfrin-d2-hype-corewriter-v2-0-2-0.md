---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-d2-hype-corewriter-v2-0-2-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-d2-hype-corewriter-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-d2-hype-corewriter-v2-0
title: Remove loop when sending actions
vuln_class: []
---

# Remove loop when sending actions

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-d2-hype-corewriter-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-d2-hype-corewriter-v2.0.md)_

---

**Description:** `Hype_Module::sendAction` manually allocates and copies a 4-byte header plus payload in a loop. Use packed encoding to avoid the loop and shrink bytecode, e.g.:

```solidity
bytes memory data = abi.encodePacked(bytes4(uint32(0x01000000) | uint32(actionIndex)), action);
```

This builds the prefix + payload in one go with lower gas and less code.

**D2:** Fixed in commit [`c5d3193`](https://github.com/d2sd2s/d2-contracts/commit/c5d319387671e889e1d1c6aaf5097b5653af6809)

**Cyfrin:** Verified.

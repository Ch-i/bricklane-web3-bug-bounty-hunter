---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-10-cyfrin-thermae-3-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-01-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-10-cyfrin-thermae.md
tags:
- firm:cyfrin
- report:2024-01-10-cyfrin-thermae
title: Remove unused code
vuln_class: []
---

# Remove unused code

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-10-cyfrin-thermae.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-10-cyfrin-thermae.md)_

---

**Description:**
```solidity
File: PorticoStructs.sol L67-79:
  //16 + 32 + 24 + 24 + 16 + 16 + 8 + 8 == 144
  struct packedData {
    uint16 recipientChain;
    uint32 bridgeNonce;
    uint24 startFee;
    uint24 endFee;
    int16 slipStart;
    int16 slipEnd;
    bool wrap;
    bool unwrap;
  }
```

**Wormhole:**
Fixed in commit 6208dd1.

**Cyfrin:** Verified.

\clearpage

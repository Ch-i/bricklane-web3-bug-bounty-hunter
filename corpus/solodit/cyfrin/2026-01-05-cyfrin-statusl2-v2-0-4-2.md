---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-4-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: '`KarmaTiers.sol` constructor can be simplified'
vuln_class: []
---

# `KarmaTiers.sol` constructor can be simplified

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** It sets owner:
```solidity
    constructor() {
        transferOwnership(msg.sender);
    }
```
However owner is already set in `Ownable.sol`:
```solidity
    constructor() {
        _transferOwnership(_msgSender());
    }
```

Same logic exists in other 2 constructors in `BaseNFTMetadataGenerator.sol` and `KarmaNFT.sol`

**Recommended Mitigation:** Remove `transferOwnership(msg.sender)` from constructor in `KarmaTiers.sol`, `KarmaNFT.sol`, `BaseNFTMetadataGenerator.sol`.

**StatusL2:** Fixed in [606e3d1](https://github.com/status-im/status-network-monorepo/commit/606e3d14a76f6568865267df0db56db5963440ca).

**Cyfrin:** Verified.

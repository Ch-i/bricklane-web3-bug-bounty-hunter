---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-2-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-bridgex-v2-0
title: Use named imports
vuln_class: []
---

# Use named imports

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** Use named imports:
```diff
PublicBridge.sol
- import "./Token.sol";
+ import {IERC20, Token} from "./Token.sol";
```

**BridgeX:**
Fixed in commit [5b5523c](https://github.com/NerdUnited-NodeGovernance/audit-2026-03-bridgex/commit/5b5523c72792d61b9c3ba11a32af246838ac9a04).

**Cyfrin:** Verified.

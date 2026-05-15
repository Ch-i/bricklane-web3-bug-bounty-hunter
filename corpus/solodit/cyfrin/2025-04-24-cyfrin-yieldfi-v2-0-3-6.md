---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-3-6
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-yieldfi-v2-0
title: Unused imports
vuln_class: []
---

# Unused imports

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-yieldfi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md)_

---

**Description:** Consider removing the following unused imports:

- contracts/bridge/Bridge.sol [Line: 7](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/Bridge.sol#L7)
- contracts/bridge/Bridge.sol [Line: 9](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/Bridge.sol#L9)
- contracts/bridge/Bridge.sol [Line: 13](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/Bridge.sol#L13)
- contracts/bridge/Bridge.sol [Line: 15](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/Bridge.sol#L15)
- contracts/bridge/Bridge.sol [Line: 18](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/Bridge.sol#L18)
- contracts/bridge/Bridge.sol [Line: 20](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/Bridge.sol#L20)
- contracts/bridge/BridgeMB.sol [Line: 17](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/BridgeMB.sol#L17)
- contracts/bridge/ccip/BridgeCCIP.sol [Line: 4](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/ccip/BridgeCCIP.sol#L4)
- contracts/bridge/ccip/BridgeCCIP.sol [Line: 13](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/bridge/ccip/BridgeCCIP.sol#L13)
- contracts/core/Manager.sol [Line: 6](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/Manager.sol#L6)
- contracts/core/Manager.sol [Line: 15](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/Manager.sol#L15)
- contracts/core/Manager.sol [Line: 17](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/Manager.sol#L17)
- contracts/core/OracleAdapter.sol [Line: 6](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/OracleAdapter.sol#L6)
- contracts/core/PerpetualBond.sol [Line: 7](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/PerpetualBond.sol#L7)
- contracts/core/PerpetualBond.sol [Line: 13](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/PerpetualBond.sol#L13)
- contracts/core/interface/IPerpetualBond.sol [Line: 4](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/interface/IPerpetualBond.sol#L4)
- contracts/core/l1/LockBox.sol [Line: 10](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/l1/LockBox.sol#L10)
- contracts/core/l1/LockBox.sol [Line: 13](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/l1/LockBox.sol#L13)
- contracts/core/l1/Yield.sol [Line: 5](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/l1/Yield.sol#L5)
- contracts/core/l1/Yield.sol [Line: 10](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/l1/Yield.sol#L10)
- contracts/core/l1/Yield.sol [Line: 11](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/l1/Yield.sol#L11)
- contracts/core/l1/Yield.sol [Line: 12](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/l1/Yield.sol#L12)
- contracts/core/l1/Yield.sol [Line: 13](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/l1/Yield.sol#L13)
- contracts/core/l1/Yield.sol [Line: 14](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/l1/Yield.sol#L14)
- contracts/core/l1/Yield.sol [Line: 16](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/l1/Yield.sol#L16)
- contracts/core/tokens/YToken.sol [Line: 8](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/tokens/YToken.sol#L8)
- contracts/core/tokens/YToken.sol [Line: 14](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/tokens/YToken.sol#L14)
- contracts/core/tokens/YTokenL2.sol [Line: 12](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/tokens/YTokenL2.sol#L12)

**YieldFi:** Fixed in commit [`8264429`](https://github.com/YieldFiLabs/contracts/commit/826442914cb9829aa302dbaef0741659cc5a1a67)

**Cyfrin:** Verified.

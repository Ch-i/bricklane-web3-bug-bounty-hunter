---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-09-cyfrin-matrixdock-v2-0-0-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-04-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-09-cyfrin-matrixdock-v2-0
title: Missing `receive` function to reject direct ETH transfers in messager contracts
vuln_class: []
---

# Missing `receive` function to reject direct ETH transfers in messager contracts

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-09-cyfrin-matrixdock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md)_

---

**Description:** The messager contracts (`MTokenMessager`, `MTokenMessagerLZ`, `MTokenMessagerV2`) are designed to receive the bridging fee in native token but none of them implemented a `receive()` function to handle direct ETH transfers. Without this function, users can accidentally send ETH to the contract address where it will be permanently locked since there's no mechanism to withdraw it.

**Recommended Mitigation:** Add a `receive()` function that reverts to explicitly reject any direct ETH transfers to the contract:

```diff
3 contract MTokenMessagerBase {
4
5     address public ccipClient;//@audit-info MToken
6
7     constructor(address _ccipClient){
8         ccipClient = _ccipClient;
9     }
+
+     receive() external payable {
+         revert("ETH transfers not accepted");
+     }
10 }
```

**Matrixdock:** Acknowledged.

---
affected_contracts: []
derives_from: []
id: solodit-hexens-2023-02-27-polygonzkevm-3-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-02-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-02-27-PolygonZkEvm.md
tags:
- firm:hexens
- report:2023-02-27-polygonzkevm
title: 12. REDUNDANT IMPORTS
vuln_class: []
---

# 12. REDUNDANT IMPORTS

_Section severity (from Solodit section header): Informational_  
_Audit firm: Hexens_  
_Source report: [2023-02-27-PolygonZkEvm.md](https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-02-27-PolygonZkEvm.md)_

---

**Severity:** Informational

**Path:** PolygonZkEVM.sol

**Description:** 

The imports for ERC20BurnableUpgradeable.sol and Initializable.sol are redundant as they are either not used or already imported recursively.

```
import "@openzeppelin/contracts-upgradeable/token/ERC20/utils/SafeERC20Upgradeable.sol";
//import "@openzeppelin/contracts-upgradeable/token/ERC20/extensions/ERC20BurnableUpgradeable.sol";   // redundant import
import "./interfaces/IVerifierRollup.sol";
import "./interfaces/IPolygonZkEVMGlobalExitRoot.sol";
//import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol"; // redundant import
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import "./interfaces/IPolygonZkEVMBridge.sol";
import "./lib/EmergencyManager.sol";

```

**Remediation:**  Remove the redundant imports.

**Status:** Fixed

- - -

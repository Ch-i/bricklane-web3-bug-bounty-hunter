---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-06-cyfrin-benqi-collateral-migrator-v2-0-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-04-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-06-cyfrin-benqi-collateral-migrator-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-06-cyfrin-benqi-collateral-migrator-v2-0
title: Unused imports
vuln_class: []
---

# Unused imports

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-06-cyfrin-benqi-collateral-migrator-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-06-cyfrin-benqi-collateral-migrator-v2.0.md)_

---

**Description:** There are two unused imports:
* [`CommonErrors`, `CollateralMigrator.sol#17`](https://github.com/woof-software/benqi-collateral-migrator/blob/d91ce3dbf56d3939d54520f6f41afeebbbfc069a/contracts/CollateralMigrator.sol#L17):
  ```solidity
  import {CommonErrors} from "./errors/CommonErrors.sol";
  ```
* [`ISwapper`, `SwapModule.sol#L6`](https://github.com/woof-software/benqi-collateral-migrator/blob/d91ce3dbf56d3939d54520f6f41afeebbbfc069a/contracts/modules/SwapModule.sol#L6):
  ```solidity
  import {ISwapper} from "../interfaces/1Inch-v6/ISwapper.sol";
  ```

Consider removing these.

**Benqi:** Fixed in commit [`34d2cca`](https://github.com/woof-software/benqi-collateral-migrator/commit/34d2ccaad91fadbd723ec0e26a7fcdc1484b8028)

**Cyfrin:** Verified.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-3-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Use named imports
vuln_class: []
---

# Use named imports

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** Use named imports; this is already being done in some places but not others:
* `Issuance`:
```solidity
minter/Minter.sol
4:import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
5:import "@openzeppelin/contracts/access/AccessControl.sol";
6:import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

vault/StakingVault.sol
5:import "../interfaces/vault/IStakingVault.sol";
7:import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

helpers/TokensHolder.sol
4:import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

token/HilBTC.sol
4:import "@openzeppelin/contracts/access/AccessControl.sol";
```

* `Deposit-Registry`:
```solidity
interfaces/ICompliantDepositRegistry.sol
4:import "@openzeppelin/contracts/access/IAccessControl.sol";
5:import "./IComplianceChecker.sol";

interfaces/IComplianceChecker.sol
4:import "@openzeppelin/contracts/access/IAccessControl.sol";
5:import "@galactica-net/zk-certificates/contracts/interfaces/IVerificationSBT.sol";

ComplianceChecker.sol
4:import "@openzeppelin/contracts/access/AccessControl.sol";
5:import "./interfaces/IComplianceChecker.sol";

CompliantDepositRegistry.sol
4:import "@openzeppelin/contracts/access/AccessControl.sol";
5:import "./interfaces/IComplianceChecker.sol";
6:import "./interfaces/ICompliantDepositRegistry.sol";
```

**Syntetika:**
Fixed in commit [a8b4853](https://github.com/SyntetikaLabs/monorepo/commit/a8b485381ad97ffb01595e8e5cc3d479126fcee8).

**Cyfrin:** Verified.

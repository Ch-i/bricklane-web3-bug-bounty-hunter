---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-23-cyfrin-soneium-shibuya-v2-0-0-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-12-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-23-cyfrin-soneium-shibuya-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-23-cyfrin-soneium-shibuya-v2-0
title: Lack of validation for default admin revocation during initialization
vuln_class: []
---

# Lack of validation for default admin revocation during initialization

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-23-cyfrin-soneium-shibuya-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-23-cyfrin-soneium-shibuya-v2.0.md)_

---

**Description:** In `ShibuyaToken::initializeV3()`, the contract attempts to revoke `DEFAULT_ADMIN_ROLE` from the provided `defaultAdmin` parameter. Based on the deployed contract on testnet and team communication, the intention was to remove the role from the original default admin address during the upgrade process.

However, the current implementation has two issues:
1. It revokes the role without first verifying if the address actually possesses the role in the previous version
2. The accompanying comments are misleading, stating "this is to make sure that the default admin is the owner and remove the default admin role from the deployer". This implies the deployer always has the default admin role, which isn't necessarily true.

```solidity
Shibuya.sol
36:         // this is to make sure that the default admin is the owner and remove the default admin role from the deployer
37:         // so this means that the deployer will not have any role in the contract
38:         // the the DEFAULT_ADMIN_ROLE will not have any role in the contract
39:         // and the owner will be performing the role of the admin
40:         _revokeRole(DEFAULT_ADMIN_ROLE, defaultAdmin);
```

Additionally, there's a typographical error in the comments at line 38 where "the" is repeated.

**Recommended Mitigation:**
- Add an explicit check if `defaultAdmin` has `DEFAULT_ADMIN_ROLE` before revoking
- Document clearly in the upgrade guide about role requirements
- Fix minor mistakes in comments

**Startale:** Fixed in commit [01789b](https://github.com/StartaleLabs/ccip-contracts-registration/commit/01789b01cb654607c91f011a3ea768ebfc486a14).

**Cyfrin:** Verified.

\clearpage

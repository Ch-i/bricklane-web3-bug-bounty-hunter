---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0-3-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-12-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0
title: Incorrect/misleading comments (2) - SecuritizeVault
vuln_class: []
---

# Incorrect/misleading comments (2) - SecuritizeVault

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md)_

---

**Description:** Comments that do not accurately reflect the code's functionality can lead to misinterpretation during development, code review, and future maintenance.
```solidity
ISecuritizeVault.sol
72:     /**
73:      * @dev Grants the Redeemer role to an account. Emits a OwnerAdded event.//@audit-issue INFO Redeemer role is not defined in the interface. Must be Owner.
74:      *
75:      * @param _account The address to which the Owner role will be granted.
76:      */
77:     function addOwner(address _account) external;

86:     /**
87:      * @dev Checks if an account has the Redeemer role.//@audit-issue INFO Redeemer role is not defined in the interface. Must be Owner.
88:      *
89:      * @param _account The address to check for the Redeemer role.
90:      * @return bool Returns true if the account has the Redeemer role, false otherwise.
91:      */
92:     function isOwner(address _account) external view returns (bool);
```

```solidity
SecuritizeVault.sol
120:     /**
121:      * @dev Grants the owner role to an account. Emits a RedeemerAdded event.//@audit-issue INFO wrong comment, should be Owner
122:      * Owners can deposit and redeem. Emits OwnerAdded event
123:      *
124:      * @param _account The address to which the Redeemer role will be granted.
125:      */
126:     function addOwner(address _account) external addressNotZero(_account) onlyRole(DEFAULT_ADMIN_ROLE) {
127:         grantRole(OWNER_ROLE, _account);
128:         emit OwnerAdded(_account);
129:     }
130:
131:     /**
132:      * @dev Revokes the Owner role from an account. Emits a OwnerRevoked event.
133:      *
134:      * @param _account The address from which the Redeemer role will be revoked.
135:      */
136:     function revokeOwner(address _account) external addressNotZero(_account) onlyRole(DEFAULT_ADMIN_ROLE) {
137:         revokeRole(OWNER_ROLE, _account);
138:         emit OwnerRevoked(_account);
139:     }

```

```solidity
SecuritizeVault.sol
320:     /**
321:      * @dev Internal conversion function (from shares to assets) with support for rounding direction.
322:      *
323:      * This function overrides the default behavior in ERC4626Upgradeable
324:      * to ensure a conversion using NavProvider rate between assets and shares.
325:      *
326:      * min (xsSHARE / NAV, xsSHARE * tSHARE / tsSHARE) // <- xsSHARE & tASSSET / tsSHARE
327:      *
328:      * For more details, view ERC4626Upgradeable documentation.
329:      *
330:      * @param _shares The amount of shares to convert to assets.
331:      * @return uint256 The equivalent amount of assets.
332:      */
```

**Securitize:** Fixed in commit [172aed](https://bitbucket.org/securitize_dev/bc-securitize-vault-sc/commits/172aed24319d7bd2224cb3182f2150d90f43ac3a).

**Cyfrin:** Verified.

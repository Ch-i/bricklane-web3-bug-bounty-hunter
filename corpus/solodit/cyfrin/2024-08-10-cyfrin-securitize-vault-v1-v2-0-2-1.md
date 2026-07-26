---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-10-cyfrin-securitize-vault-v1-v2-0-2-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-08-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-10-cyfrin-securitize-vault-v1-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-10-cyfrin-securitize-vault-v1-v2-0
title: Some comments are misleading
vuln_class: []
---

# Some comments are misleading

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-10-cyfrin-securitize-vault-v1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-10-cyfrin-securitize-vault-v1-v2.0.md)_

---

**Description:** Some comments are wrong/misleading.

In the below snippet, `impairedAssetBalance` is not a flag, it was supposed to be the function `impairedAsset()`.
```solidity
SecuritizeVault.sol
177: * - The `impairedAssetBalance` flag must be true, indicating that the asset balance is indeed impaired.
```

The comment in the below snippet is incorrect (L321) because there is no possibility that the vault contract transfers assets directly to users.
```solidity
SecuritizeVault.sol
320:      * This can occur if users transfer assets directly to the vault instead of using the deposit function,
321:      * or if the vault transfers assets directly to users instead of using the redeem function.
```

**Securitize:** Fixed in [a2bae8](https://bitbucket.org/securitize_dev/bc-securitize-vault-sc/commits/a2bae865466a79c9a079a0957efa05ea0d6f68a6) and [b337b1](https://bitbucket.org/securitize_dev/bc-securitize-vault-sc/commits/b337b1271b72c5d53e46412c734672c45afc6039).

**Cyfrin:** Verified.

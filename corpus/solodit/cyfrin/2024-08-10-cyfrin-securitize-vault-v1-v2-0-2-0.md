---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-10-cyfrin-securitize-vault-v1-v2-0-2-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-08-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-10-cyfrin-securitize-vault-v1-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-10-cyfrin-securitize-vault-v1-v2-0
title: Some function names are misleading
vuln_class: []
---

# Some function names are misleading

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-10-cyfrin-securitize-vault-v1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-10-cyfrin-securitize-vault-v1-v2.0.md)_

---

**Description:** Some function names are misleading given the usages.

- The modifier `receiverSenderNotEqual()` is used to ensure the `msg.sender` is equal to the argument and the name that includes the parameter name is not desirable here, especially given that the same modifier is used to check if the `msg.sender==owner` at L273.
`senderEqualTo` or `msgSenderEqualTo` would be better.
```solidity
37: modifier receiverSenderNotEqual(address _receiver) {
38:         require(_receiver == msg.sender, "Receiver must be equal to sender");
39:         _;
40:     }
```
- `assetIsImpaired()` is better than `impairedAsset()` given that this function does not return the actual impaired amount but the status as boolean.
- `vaultIsImpaired()` is better than `impairedVault()`.

**Securitize:** Fixed in [b337b12](https://bitbucket.org/securitize_dev/bc-securitize-vault-sc/commits/b337b1271b72c5d53e46412c734672c45afc6039).

**Cyfrin:** Verified.

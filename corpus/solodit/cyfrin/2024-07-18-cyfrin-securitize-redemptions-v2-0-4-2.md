---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-18-cyfrin-securitize-redemptions-v2-0-4-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-07-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-18-cyfrin-securitize-redemptions-v2-0
title: Wrong/misleading comments
vuln_class: []
---

# Wrong/misleading comments

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-18-cyfrin-securitize-redemptions-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-18-cyfrin-securitize-redemptions-v2.0.md)_

---

**Description:** In multiple locations, comments are wrong or misleading. These wrong/misleading comments can lead to unexpected interpretation of the contract and potential security issues. We recommend fix these wrong or misleading comments.

```solidity
ISecuritizeNavProvider.sol
6:  * @dev Defines a common interface to get NAV (Native Asset Value) Rate to //@audit Incomplete comment

SecuritizeInternalNavProvider.sol
9:      * @dev rate: NAV rate expressed with 6 decimals//@audit-issue INFO incomplete comment
14:     * @dev Throws if called by any account other than the owner.//@audit-issue INFO wrong comment

SecuritizeRedemption.sol
26: * @dev Emitted when the Settlement address changes//@audit-issue INFO wrong comment

BaseSecuritizeSwap.sol
98: * @param sigR R signature//@audit-issue INFO wrong comment, should be sigS

BaseSecuritizeSwap.sol
102: * @param params array of params. params[0] = value, params[1] = gasLimit, params[2] = blockLimit//@audit-issue INFO wrong comment, params length is two

SecuritizeSwap.sol
131: * @param sigR R signature//@audit-issue INFO wrong comment, should be sigS

IDSToken.sol
16: * @param _cap address The address which is going to receive the newly issued tokens//@audit-issue INFO wrong comment
```

**Securitize:** Fixed in commit [3977ca](https://bitbucket.org/securitize_dev/bc-redemption-sc/commits/3977ca8ffb259a01e8dab894745751cf2150abf4), [b09460](https://bitbucket.org/securitize_dev/securitize-swap/commits/b094604b341123a49c8abbd6e1c3d53d7c102f28), and [334f49](https://bitbucket.org/securitize_dev/bc-nav-provider-sc/commits/334f4996bc79d0489122210ed54c5596bdcf4eb7).

**Cyfrin:** Verified.


\clearpage

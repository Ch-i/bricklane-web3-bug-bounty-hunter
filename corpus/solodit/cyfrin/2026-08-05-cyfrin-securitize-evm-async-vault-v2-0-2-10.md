---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-05-cyfrin-securitize-evm-async-vault-v2-0-2-10
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-08-05T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-05-cyfrin-securitize-evm-async-vault-v2-0
title: Cancellation functions do not support an alternative recipient
vuln_class: []
---

# Cancellation functions do not support an alternative recipient

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md)_

---

**Description:** Both cancellation functions always return tokens directly to the controller:

```solidity
// Deposit cancellation
$.liquidityToken.safeTransfer(controller, amount);

// Redemption cancellation
IERC20(address($.dsToken)).safeTransfer(controller, amount);
```

Neither function allows the caller to specify another recipient, unlike claim functions such as `deposit()` and `redeem()`.

If the controller is blocked from receiving the liquidity token or DS Token, the corresponding cancellation reverts. The user can wait for fulfillment, but cannot redirect the cancelled tokens to another valid address.

**Recommended Mitigation:** Add a recipient parameter to both cancellation functions.

**Securitize:** Fixed in commit [a97c952](https://github.com/securitize-io/bc-async-ramp-sc/commit/a97c9525dccddd3f617e34956a68c12fb0bb595c).

**Cyfrin:** Verified.


\clearpage

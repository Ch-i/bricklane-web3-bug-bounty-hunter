---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-19-lyra-finance-1-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-01-19T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md
tags:
- firm:trust-security
- report:2023-01-19-lyra-finance
title: TRST-M-5 recoverFunds() does not handle popular ERC20 tokens like BNB
vuln_class: []
---

# TRST-M-5 recoverFunds() does not handle popular ERC20 tokens like BNB

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-01-19-Lyra Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md)_

---

**Description:** 
recoverFunds() is used for recovery in case of mistakenly-sent tokens. However, it uses unsafe 
transfer to send tokens back, which will not support 100s of non-compatible ERC20 tokens. 
Therefore it is likely unsupported tokens will be unrecoverable.
```solidity
  if (token == quoteAsset || token == baseAsset || token == weth) {
      revert CannotRecoverRestrictedToken(address(this));
    }
        token.transfer(recipient, token.balanceOf(address(this)));
```

**Recommended Mitigation:**
Use Open Zeppelin’s SafeERC20 encapsulation of ERC20 transfer functions.

**Team response:**
This function exists purely as an additional recovery mechanism that should never really be 
used - it is not core to the functionality of the protocol. Will not be changed at this stage.

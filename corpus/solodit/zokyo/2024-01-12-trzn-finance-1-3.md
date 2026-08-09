---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-1-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: Require check in `MultiSig_V2` can be bypassed
vuln_class: []
---

# Require check in `MultiSig_V2` can be bypassed

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: Medium

**Status**:  Resolved

**Description**

In the MultiSig contract, the require check statement of `_numConfirmationsRequired <= _whiteWallet.length` could be bypassed if `DeregisterWhiteWallet()` is used. For example, if the wallet `_whiteWallet.length` is 3 and the `_numConfirmationsRequired` is also 3, it is possible that `DeregisterWhiteWallet()` would be called in future. 

After the call, the `_numConfirmationsRequired` would become 3 whereas the `_whiteWallet.length` would be 2, which would be a violation of the statement in constructor which tries to ensure that `_numConfirmationsRequired <= _whiteWallet.length`.
```solidity
         require(
            _numConfirmationsRequired > 0 &&
                _numConfirmationsRequired <= _whiteWallet.length,
            "invalid number of required confirmations"
        );
```

**Recommendation**: It is advised to add an internal function that decreases the `_numConfirmationsRequired` accordingly in the `DeregisterWhiteWallet()` function.

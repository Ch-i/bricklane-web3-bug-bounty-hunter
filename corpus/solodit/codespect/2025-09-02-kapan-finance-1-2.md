---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-09-02-kapan-finance-1-2
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-09-02T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-09-02-Kapan-Finance.md
tags:
- firm:codespect
- report:2025-09-02-kapan-finance
title: '[M-03] The on_flash_loan(...) function lacks a caller verification check'
vuln_class: []
---

# [M-03] The on_flash_loan(...) function lacks a caller verification check

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2025-09-02-Kapan-Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-09-02-Kapan-Finance.md)_

---

**Files:** [`RouterGateway.cairo`](https://github.com/StefanIliev545/kapan/tree/83a7747df3350c2b23d747d52bdd998adbc8812d/packages/snfoundry/contracts/src/gateways/RouterGateway.cairo)

**Description:**

The `on_flash_loan` function is the flash loan callback function. After receiving the flash loan, the contract executes instruction logic within `on_flash_loan`. However, since there is no check to ensure that the caller is the `flashloan_provider`, a malicious actor can arbitrarily call this function to bypass the `ensure_user_matches_caller` check and execute instructions.

```cairo
fn on_flash_loan(...) {
    assert(sender == get_contract_address(), 'sender mismatch');
    println!("Received flash loan");
    //...
}
```

**Impact:** This could potentially lead to the theft of tokens that users have approved for the Router contract — For example, if a user wants to withdraw from NostraGateway via the router, they need to approve `nibcollateral` to the router. A malicious actor can check for such approvals. Then call `on_flash_loan` to execute the withdraw instruction, and then call the deposit instruction to steal those tokens.

**Recommendation:** It is recommended to check whether the caller is the flashloan provider.

**Status:** Fixed

---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-09-02-kapan-finance-1-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-09-02T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-09-02-Kapan-Finance.md
tags:
- firm:codespect
- report:2025-09-02-kapan-finance
title: '[M-02] Repay may fail due to insufficient tokens approval'
vuln_class: []
---

# [M-02] Repay may fail due to insufficient tokens approval

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2025-09-02-Kapan-Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-09-02-Kapan-Finance.md)_

---

**Files:** [`NostraGateway.cairo`](https://github.com/StefanIliev545/kapan/tree/83a7747df3350c2b23d747d52bdd998adbc8812d/packages/snfoundry/contracts/src/gateways/NostraGateway.cairo), [`RouterGateway.cairo`](https://github.com/StefanIliev545/kapan/tree/83a7747df3350c2b23d747d52bdd998adbc8812d/packages/snfoundry/contracts/src/gateways/RouterGateway.cairo)

**Description:**

If the `repay_all` field is enabled in the repay instruction, it is expected to repay all outstanding debt. However, since this value does not overwrite the `amount` field in the repay instruction within `instructions`.

```cairo
fn before_send_instructions(...) -> Span<u256> {
    //...
    LendingInstruction::Repay(repay) => {
        let basic = *repay.basic;
        let erc20 = IERC20Dispatcher { contract_address: basic.token };
        if should_transfer {
            assert(
                erc20.transfer_from(
                    get_caller_address(), get_contract_address(), basic.amount,
                ),
                'transfer failed',
            );
        }
        assert(erc20.approve(gateway, basic.amount), 'approve failed');
        let balance = erc20.balance_of(get_contract_address());
        balancesBefore.append(balance);
    },
```

**Impact:** It may result in a failed repayment in `before_send_instructions` due to insufficient approval or token transfer. For example, if the `repay_all` flag is enabled but the `repay.amount` is arbitrarily set to a value like 1, then `before_send_instructions` will not transfer a sufficient amount of tokens to the Router, and the Router will not approve enough allowance to the Gateway, resulting in the repay operation failing.

**Recommendation:** In `before_send_instructions`, before transferring and approving tokens for a repay instruction, check if `repay_all` is enabled. If it is, replace the operation amount with the corresponding total debt amount instead of using `repay.amount`.

**Status:** Fixed

---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-09-02-kapan-finance-3-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-09-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-09-02-Kapan-Finance.md
tags:
- firm:codespect
- report:2025-09-02-kapan-finance
title: '[I-01] Revoke excess approvals in after_send_instructions(...)'
vuln_class: []
---

# [I-01] Revoke excess approvals in after_send_instructions(...)

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-09-02-Kapan-Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-09-02-Kapan-Finance.md)_

---

**Original severity:** Best Practices

**Files:** [`RouterGateway.cairo`](https://github.com/StefanIliev545/kapan/tree/83a7747df3350c2b23d747d52bdd998adbc8812d/packages/snfoundry/contracts/src/gateways/NostraGateway.cairo)

**Description:**

In `after_send_instructions`, there may be cases where not all tokens are used during repayment because `repay.amount > debt`. The unused tokens will be transferred from the router to the user. However, the approval for these tokens granted to the gateway in `before_send_instructions` has not yet been revoked.

```cairo
fn after_send_instructions(
    ref self: ContractState,
    gateway: ContractAddress,
    instructions: Span<LendingInstruction>,
    balancesBefore: Span<u256>,
    should_transfer: bool,
) -> Span<u256> {
    // ...
    LendingInstruction::Repay(repay) => {
        let basic = *repay.basic;
        let erc20 = IERC20Dispatcher { contract_address: basic.token };
        let balance = erc20.balance_of(get_contract_address());
        let diff = *balancesBefore.at(i) - balance;
        balancesAfter.append(diff);
        if basic.amount > diff {
            let erc20 = IERC20Dispatcher { contract_address: basic.token };
            erc20.transfer(basic.user, basic.amount - diff);
        }
    },
    // ...
}
```

**Impact:** A user can manipulate the system to cause the router to grant an excessively large approval to the gateway. For example, if `user1` only has a debt of 10 but sets `repay.amount` to 10,000 during repayment, the unused 9,990 tokens will be returned to `user1`. However, the router’s approval of 9,990 tokens to the gateway remains in place.

While this may not have an immediate visible impact, it is recommended to revoke this unused approval to reduce the potential attack surface in future updates.

**Recommendation:** It is recommended to revoke the router’s approval to the gateway for the refunded tokens.

**Status:** Fixed

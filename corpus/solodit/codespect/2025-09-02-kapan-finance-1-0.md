---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-09-02-kapan-finance-1-0
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
title: '[M-01] Certain instruction combos create negative balancesAfter and will revert'
vuln_class: []
---

# [M-01] Certain instruction combos create negative balancesAfter and will revert

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2025-09-02-Kapan-Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-09-02-Kapan-Finance.md)_

---

**Files:** [`RouterGateway.cairo`](https://github.com/StefanIliev545/kapan/tree/83a7747df3350c2b23d747d52bdd998adbc8812d/packages/snfoundry/contracts/src/gateways/RouterGateway.cairo)

**Description:**

Through the RouterGateway contract, users can choose to execute multiple sequential instructions on a single gateway. Before executing the instructions, the contract checks its token balances. After execution, it checks its token balances again and calculates the difference from the first check. However, this difference may be a negative value, which will result in the transaction reverting since `balancesAfter` is an array of `u256`.

For example:

1. Deposit 100 of token1;
2. Borrow 100 of token1;

Since 100 tokens are transferred into the contract in advance, `balanceBefore = [100, 100]`.

Looking at `balancesAfter` calculation for these 2 instructions:

```cairo
fn after_send_instructions(
    ref self: ContractState,
    gateway: ContractAddress,
    instructions: Span<LendingInstruction>,
    balancesBefore: Span<u256>,
    should_transfer: bool,
) -> Span<u256> {
    let mut i: usize = 0;
    let mut balancesAfter = array![];
    while i != instructions.len() {
        match instructions.at(i) {
            LendingInstruction::Borrow(borrow) => {
                let basic = *borrow.basic;
                let erc20 = IERC20Dispatcher { contract_address: basic.token };
                if should_transfer {
                    assert(
                        erc20
                            .transfer(
                                basic.user, erc20.balance_of(get_contract_address()),
                            ),
                        'transfer failed',
                    );
                }
                let balance = erc20.balance_of(get_contract_address());

                balancesAfter.append(balance - *balancesBefore.at(i));
            },
            ...

            LendingInstruction::Deposit(deposit) => {
                let basic = *deposit.basic;
                let erc20 = IERC20Dispatcher { contract_address: basic.token };
                let balance = erc20.balance_of(get_contract_address());
                balancesAfter.append(*balancesBefore.at(i) - balance);
            },
            _ => {},
        }
        i += 1;
    }
    balancesAfter.span()
}
```

Here Borrow will first transfer the 100 borrowed tokens to the user and then track the balance of the contract. As a result, `balanceAfter` here will be attempted to be `0 - 100` and transaction will revert.

**Impact:** Certain instruction combinations will have a negative value for `balanceAfter` and will result in the transaction reverting.

**Status:** Fixed

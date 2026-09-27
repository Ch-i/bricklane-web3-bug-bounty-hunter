---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-09-02-kapan-finance-0-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-09-02T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-09-02-Kapan-Finance.md
tags:
- firm:codespect
- report:2025-09-02-kapan-finance
title: '[H-01] Certain combinations of instructions can lead to token loss'
vuln_class: []
---

# [H-01] Certain combinations of instructions can lead to token loss

_Section severity (from Solodit section header): High_  
_Audit firm: CODESPECT_  
_Source report: [2025-09-02-Kapan-Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-09-02-Kapan-Finance.md)_

---

**Files:** [`RouterGateway.cairo`](https://github.com/StefanIliev545/kapan/tree/83a7747df3350c2b23d747d52bdd998adbc8812d/packages/snfoundry/contracts/src/gateways/RouterGateway.cairo)

**Description:**

Through the RouterGateway contract, users can choose to execute multiple sequential instructions on a single gateway. Before executing the instructions, the contract checks its token balances. After execution, it calculates the balance changes and transfers tokens to the user accordingly. However, since the pre-execution balance includes tokens that are meant to be input (e.g., for deposit or repay), certain combinations of instructions may result in token loss.

```cairo
fn before_send_instructions(...) -> Span<u256> {
    let mut i: usize = 0;
    let mut balancesBefore = array![];
    while i != instructions.len() {
        match instructions.at(i) {
            LendingInstruction::Deposit(deposit) => {
                let basic = *deposit.basic;
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
            //...
```

Some combinations of instructions may lead to token loss. For example:

1. repay token1 with 100;
2. withdraw to retrieve 110 of token1;

Since 100 token1 tokens are input into the contract in advance, `balanceBefore = [100, 100]`. During execution, 100 token1 tokens are used to repay the debt, and the withdraw retrieves 110 tokens. `balanceAfter = 110 - 100 = 10`. Only 10 token1 tokens are sent to the user, while the remaining 100 tokens remain locked in the contract.

**Impact:** Certain instructions combinations that use the same token can lead to permanent loss.

**Recommendation:** It is recommended that `after_send_instructions` fetch the token balances before any token inputs occur, and then iterate through the instructions to execute token inputs.

**Status:** Fixed

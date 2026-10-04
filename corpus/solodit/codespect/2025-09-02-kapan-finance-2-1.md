---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-09-02-kapan-finance-2-1
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-09-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-09-02-Kapan-Finance.md
tags:
- firm:codespect
- report:2025-09-02-kapan-finance
title: '[L-02] The on_flash_loan(...) function does not take the repay_all flag into
  account when handling the repay instruction'
vuln_class: []
---

# [L-02] The on_flash_loan(...) function does not take the repay_all flag into account when handling the repay instruction

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-09-02-Kapan-Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-09-02-Kapan-Finance.md)_

---

**Files:** [`RouterGateway.cairo`](https://github.com/StefanIliev545/kapan/tree/83a7747df3350c2b23d747d52bdd998adbc8812d/packages/snfoundry/contracts/src/gateways/RouterGateway.cairo)

**Description:**

In the `on_flash_loan` function, funds are obtained via flash loan to prepare for debt repayment. The total repay amount is recalculated and the repay instruction is reconstructed. However, since the `repay_all` flag is not taken into account, some of these checks may become invalid.

```cairo
fn on_flash_loan(...) {
    //...
    for protocolInstruction in protocol_instructions {
        for instruction in protocolInstruction.instructions {
            if let LendingInstruction::Repay(repay) = instruction {
                let repay = *repay;
                repay_amounts.append(repay.basic.amount);
                total_repay_amount += repay.basic.amount;
                repay_count += 1;
            }
        }
    }

    // Calculate remaining amount to distribute
    let remaining_amount = amount - total_repay_amount;
    assert(remaining_amount >= 0, 'flashloan insufficient');
    //...
    for instruction in protocol_instructions {
        //...
        basic: BasicInstruction {
            token: repay.basic.token,
            amount: modified_amount,
            user: repay.basic.user,
        },
        repay_all: false, // Force explicit amount
        context: repay.context,

        //...
```

When determining the flash loan amount, if the `repay_all` flag is enabled in the repay instruction, the flash loan amount is treated as the full debt rather than `repay.amount`.

However, in the `on_flash_loan` function, during validation and instruction reconstruction, `repay.amount` is used without handling the `repay_all` flag explicitly. This may lead to invalid or ineffective checks.

**Impact:** If `repay_all` is enabled and `repay.amount` does not match the full debt amount, then the `move_debt` function may fail.

**Recommendation:** The `on_flash_loan` function should consider the `repay_all` flag when accumulating amounts and reconstructing repay instructions.

**Status:** Fixed

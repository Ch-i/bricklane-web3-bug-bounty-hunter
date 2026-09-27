---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-09-02-kapan-finance-2-2
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-09-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-09-02-Kapan-Finance.md
tags:
- firm:codespect
- report:2025-09-02-kapan-finance
title: '[L-03] get_flash_loan_amount(...) may fail to return the correct amount'
vuln_class: []
---

# [L-03] get_flash_loan_amount(...) may fail to return the correct amount

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-09-02-Kapan-Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-09-02-Kapan-Finance.md)_

---

**Files:** [`RouterGateway.cairo`](https://github.com/StefanIliev545/kapan/tree/83a7747df3350c2b23d747d52bdd998adbc8812d/packages/snfoundry/contracts/src/gateways/RouterGateway.cairo)

**Description:**

In the `get_flash_loan_amount(...)` function, if a repay instruction has the `repay_all` flag enabled, the function will immediately return the flash loan amount for the gateway. However, the function does not consider whether the other `ProtocolInstructions` also contains a repay instruction.

```cairo
fn get_flash_loan_amount(...) {
    let mut flash_loan_amount: u256 = 0;
    let mut token: ContractAddress = Zero::zero();
    for protocolInstruction in instructions {
        for instruction in protocolInstruction.instructions {
            if let LendingInstruction::Repay(repay) = instruction {
                assert(*repay.basic.amount != 0, 'repay-amount-is-zero');
                if *repay.repay_all {
                    let gateway = ILendingInstructionProcessorDispatcher {
                        contract_address: self.gateways.read(*protocolInstruction.protocol_name),
                    };
                    return (*repay.basic.token, gateway.get_flash_loan_amount(*repay));
                }
                flash_loan_amount += *repay.basic.amount;
                token = *repay.basic.token;
            }
        };
    };
    //...
}
```

**Impact:** If there are multiple `ProtocolInstructions` in the array and one of the repay instructions has the `repay_all` flag enabled, due to the absence of the required amount in other repay instructions, the flash loan amount will be insufficient, causing the `move_debt` instruction to fail.

**Recommendation:** When the `repay_all` flag is enabled, do not consider the flash loan amount required for just a single market.

**Status:** Fixed

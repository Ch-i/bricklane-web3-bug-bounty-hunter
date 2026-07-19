---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-2-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-07-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-10-cyfrin-casimir-v2-0
title: Operator can set his operatorID status to active by transferring 0 Wei
vuln_class: []
---

# Operator can set his operatorID status to active by transferring 0 Wei

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-10-cyfrin-casimir-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md)_

---

**Description:** When withdrawing collateral, logic checks if collateral balance is 0 & makes the operator Id inactive.

```solidity
 function withdrawCollateral(uint64 operatorId, uint256 amount) external {
        onlyOperatorOwner(operatorId);

        Operator storage operator = operators[operatorId];
        uint256 availableCollateral = operator.collateralBalance - operator.validatorCount * collateralUnit; //@note can cause underflow here if validator count > 0
        if (availableCollateral < amount) {
            revert InvalidAmount();
        }

        operator.collateralBalance -= amount;
        if (operator.collateralBalance == 0) {
            operator.active = false;
        }

        (bool success,) = msg.sender.call{value: amount}("");
        if (!success) {
            revert TransferFailed();
        }

        emit CollateralWithdrawn(operatorId, amount);
    }

```

However while depositing, there is no check on the amount deposited. An operator can deposit 0 Wei and set operatorID to active. Deposit and withdrawal states are inconsistent.

```solidity
     function depositCollateral(uint64 operatorId) external payable {
        onlyOperatorOwner(operatorId);

        Operator storage operator = operators[operatorId];
        if (!operator.registered) {
            operatorIds.push(operatorId);
            operator.registered = true;
            emit OperatorRegistered(operatorId);
        }
        if (!operator.active) {
>            operator.active = true; //@audit -> can make operator active even with 0 wei
        }
        operator.collateralBalance += msg.value;

        emit CollateralDeposited(operatorId, msg.value);
    }**
```

**Impact:** Inconsistent logic when adding and removing validators.

**Recommended Mitigation:** Consider checking that collateral amount in the `depositCollateral` function

**Casimir:**
Fixed in [109cf2a](https://github.com/casimirlabs/casimir-contracts/commit/109cf2af2c6009e4dfa483317f2f186c97ed9da3)

**Cyfrin:** Verified.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-23-cyfrin-strata-shares-cooldown-v2-0-0-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-01-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-23-cyfrin-strata-shares-cooldown-v2-0
title: APR Targets are not updated when withdrawal requests are sent to the `SharesCooldown`
  to reflect the change on NAVs caused by the charged fees for the withdrawal
vuln_class: []
---

# APR Targets are not updated when withdrawal requests are sent to the `SharesCooldown` to reflect the change on NAVs caused by the charged fees for the withdrawal

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md)_

---

**Description:** The execution path for processing a withdrawal request sent to the `SharesCooldown` charges fees based on the total Tranche Shares redeemed. These fees are charged in the form of burning tranche shares and updating the Tranche NAV and `reserveNav` accordingly.
- `SharesCooldown::requestRedeem` => `SharesCooldown::accrueFee` => `Tranche::burnSharesAsFee` => `CDO::accrueFee` => `Accounting::accrueFee`

The problem is that the APR Targets for the Tranches are not recalculated to reflect the changes to the NAVs, which means the system will use outdated APR targets until a new operation is performed that updates the APRs.
```solidity

//Tranche::burnSharesAsFee//
    function burnSharesAsFee(uint256 shares, address owner) external returns (uint256 assets) {
        ...
        cdo.accrueFee(address(this), assets);
    }

//CDO::accrueFee//
    function accrueFee (address tranche, uint256 assets) external onlyTranche {
        accounting.accrueFee(isJrt(tranche), assets);
    }

//Accounting::accrueFee//
    function accrueFee (bool isJrt, uint256 amount) external onlyCDO {
        ...

 //@audit-issue => navs are modified, but the APRs are not updated!

        reserveNav += amountToReserve;
        if (isJrt) {
            jrtNav -= amountToReserve;
        } else {
            srtNav -= amountToReserve;
        }
        emit FeeAccrued(isJrt, amountToReserve, amount - amountToReserve);
    }
```

**Impact:** Outdated APR targets, especially outdated and higher than actual APR Targets for the SR Tranche, will cause the JRs to earn less interest than they should.

**Recommended Mitigation:** Consider refactoring the `Accounting::accrueFee` function to update the APR Target, similar to how the `Accounting::updateBalanceFlow` does.

**Strata:** Fixed in commit [b11016c](https://github.com/Strata-Money/contracts-tranches/commit/b11016c052b9b2a89a60ed6c4502c8bd94fbbea8).

**Cyfrin:** Verified. `Tranche::burnSharesAsFee` now extends the full accounting flow, updating APRs as needed.

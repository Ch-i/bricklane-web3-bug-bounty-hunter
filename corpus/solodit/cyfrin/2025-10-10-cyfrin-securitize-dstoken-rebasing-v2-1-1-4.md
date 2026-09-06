---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-1-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: No way to revert `setInvestorLiquidateOnly`
vuln_class: []
---

# No way to revert `setInvestorLiquidateOnly`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** The `setInvestorLiquidateOnly` function in `InvestorLockManagerBase.sol` contains a logic error that prevents the disabling of liquidate-only mode once it has been enabled. The function includes a require statement that checks if the investor is already in liquidate-only mode and reverts if they are, making it impossible to toggle the state back to false.

``` solidity
function setInvestorLiquidateOnly(string memory _investorId, bool _enabled) public onlyTransferAgentOrAbove returns (bool) {
    require(!investorsLiquidateOnly[_investorId], "Investor is already in liquidate only mode");
    investorsLiquidateOnly[_investorId] = _enabled;
    emit InvestorLiquidateOnlySet(_investorId, _enabled);
    return true;
}
```

**Impact:** Once an investor is set to liquidate-only mode, there is no way to disable this state


**Recommended Mitigation:** Remove the require statement to allow toggling of the liquidate-only state:

```diff
function setInvestorLiquidateOnly(string memory _investorId, bool _enabled) public onlyTransferAgentOrAbove returns (bool) {
-   require(!investorsLiquidateOnly[_investorId], "Investor is already in liquidate only mode");
    investorsLiquidateOnly[_investorId] = _enabled;
    emit InvestorLiquidateOnlySet(_investorId, _enabled);
    return true;
}
```

**Securitize:** Fixed in commit [74a6675](https://github.com/securitize-io/dstoken/commit/74a66753c15a2cdddc41a29ae8d736711b141939) by reverting if the current state is the same as the input state; this allows state to be toggled on/off.

**Cyfrin:** Verified.

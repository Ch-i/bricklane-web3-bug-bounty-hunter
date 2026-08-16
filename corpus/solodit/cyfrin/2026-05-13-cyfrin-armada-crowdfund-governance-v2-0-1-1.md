---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-1-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`ArmadaTreasuryGov` can''t distribute ETH'
vuln_class: []
---

# `ArmadaTreasuryGov` can't distribute ETH

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `ArmadaTreasuryGov` is supposed to contain protocol's funds. Specification mentions ETH among other tokens.

Problem is there is no function to distribute ETH. There is only `transferETHTo` for wind-down scenario. Moreover contract is not upgradeable, so such functionality can't be added later.

**Spec-Intent Gap:**

`specs/GOVERNANCE.md` §Treasury Distributions (Pre-wind-down):

> **Standard governance proposals:** Any treasury distribution (**ARM, USDC, ETH, other assets**) can be proposed through normal governance. Subject to treasury outflow limits.

The spec explicitly mandates a governance-gated pre-wind-down ETH spend path. Code has none. `specs/GOVERNANCE.md` §Revenue Counter Mechanism further contemplates ETH as a revenue source ("Non-stablecoin fees (ETH, etc.) require a governance proposal to attest the USD value ... and credit it to the RevenueCounter"), so the inflow is realistic.

**Recommended Mitigation:** Add `distributeETH` mirroring `distribute` with outflow-limit enforcement against `address(0)`:

```solidity
function distributeETH(address payable recipient, uint256 amount) external onlyOwner {
    require(recipient != address(0), "ArmadaTreasuryGov: zero recipient");
    require(amount > 0, "ArmadaTreasuryGov: zero amount");
    _checkAndRecordOutflow(address(0), amount);
    (bool ok,) = recipient.call{value: amount}("");
    require(ok, "ArmadaTreasuryGov: ETH transfer failed");
    emit DirectDistribution(address(0), recipient, amount);
}
```

Register the selector in `standardSelectors` and initialise an outflow config for `address(0)`. Removing `receive()` instead is not viable — spec contemplates ETH revenue.

**Armada:** Fixed in commits [0df9e56](https://github.com/ship-armada/armada-poc/commit/0df9e5652959651256242d17a1d5fc49b958ae6c), [5268148](https://github.com/ship-armada/armada-poc/commit/526814841be510434bd2174bb5aabdb36638c455).

**Cyfrin:** Verified.

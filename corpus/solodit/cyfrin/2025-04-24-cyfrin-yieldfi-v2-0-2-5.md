---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-2-5
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-yieldfi-v2-0
title: Missing vesting check in `PerpetualBond::setVestingPeriod`
vuln_class: []
---

# Missing vesting check in `PerpetualBond::setVestingPeriod`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-yieldfi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md)_

---

**Description:** Both `YToken` and `PerpetualBond` support reward vesting through a configurable vesting period. The admin can update this period via the `setVestingPeriod` function. However, there is an inconsistency in how the two contracts validate changes to the vesting period:

- [`YToken::setVestingPeriod`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/tokens/YToken.sol#L52-L56) includes a check to ensure that no rewards are currently vesting:
  ```solidity
  function setVestingPeriod(uint256 _vestingPeriod) external onlyAdmin {
      require(getUnvestedAmount() == 0, "!vesting");
      require(_vestingPeriod > 0, "!vestingPeriod");
      vestingPeriod = _vestingPeriod;
  }
  ```

- [`PerpetualBond::setVestingPeriod`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/PerpetualBond.sol#L184-L188) lacks this check:
  ```solidity
  function setVestingPeriod(uint256 _vestingPeriod) external onlyAdmin {
      // @audit-issue no check for `getUnvestedAmount() == 0`
      require(_vestingPeriod > 0, "!vestingPeriod");
      vestingPeriod = _vestingPeriod;
      emit VestingPeriodUpdated(_vestingPeriod);
  }
  ```

This means the vesting period in `PerpetualBond` can be modified even while tokens are still vesting, which could lead to inconsistent or unexpected vesting behavior.

**Recommended Mitigation:** To align with the `YToken` implementation and ensure consistency, add a check in `PerpetualBond::setVestingPeriod` to ensure `getUnvestedAmount() == 0` before allowing updates to the vesting period.

**YieldFi:** Fixed in commit [`f0bf88c`](https://github.com/YieldFiLabs/contracts/commit/f0bf88cb51a92a119cdde896c4b0118be1d1a031)

**Cyfrin:** Verified. `unvestedAmount` is now checked.

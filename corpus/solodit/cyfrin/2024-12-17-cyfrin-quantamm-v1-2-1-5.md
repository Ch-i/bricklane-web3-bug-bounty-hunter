---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-17-cyfrin-quantamm-v1-2-1-5
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-12-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md
tags:
- firm:cyfrin
- report:2024-12-17-cyfrin-quantamm-v1-2
title: '`QuantAMMBaseAdministration::onlyExecutor` modifier does not enforce a time
  lock on actions'
vuln_class: []
---

# `QuantAMMBaseAdministration::onlyExecutor` modifier does not enforce a time lock on actions

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-17-cyfrin-quantamm-v1.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md)_

---

**Description:** In `QuantAMMBaseAdministration`, certain functions are restricted using the [`onlyExecutor`](https://github.com/QuantAMMProtocol/QuantAMM-V1/blob/7213401491f6a8fd1fcc1cf4763b15b5da355f1c/pkg/pool-quantamm/contracts/QuantAMMBaseAdministration.sol#L77-L81) modifier:
```solidity
// Modifier to check for EXECUTOR_ROLE using `timelock`
modifier onlyExecutor() {
    require(timelock.hasRole(timelock.EXECUTOR_ROLE(), msg.sender), "Not an executor");
    _;
}
```
The issue with this modifier is that it does not enforce a timelock on the actions. Instead, it only verifies that the caller has the `EXECUTOR_ROLE` on the timelock contract. As seen in the OpenZeppelin [`TimelockController` code](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v5.0/contracts/governance/TimelockController.sol#L351-L371), this check allows anyone with the `EXECUTOR_ROLE` to bypass the timelock and execute commands directly on `QuantAMMBaseAdministration`.

**Impact:** Anyone with permission to execute actions on the timelock contract can bypass the timelock and execute the same commands directly on the `QuantAMMBaseAdministration` contract. This undermines the purpose of the timelock, which is to provide a delay for critical actions.

**Recommended Mitigation:**
1. **Modify the `onlyExecutor` Modifier to Enforce Timelock:**
   Change the `onlyExecutor` modifier to require that the caller is the timelock contract itself:

   ```solidity
   modifier onlyTimelock() {
       require(address(timelock) == msg.sender, "Only timelock");
       _;
   }
   ```

2. **Make `timelock` Public:**
   To allow querying the timelock's address for proposing actions, make the `timelock` variable `public`:

   ```diff
   - TimelockController private timelock;
   + TimelockController public timelock;
   ```

3. **Alternative Solution:**
   Instead of using `QuantAMMBaseAdministration`, consider using the OpenZeppelin `TimelockController` contract directly as `quantammAdmin`. This approach streamlines the process and ensures timelock enforcement without redundant checks.

**QuantAMM:** Fixed in [`a299ce7`](https://github.com/QuantAMMProtocol/QuantAMM-V1/commit/a299ce72076b58503386bc146b81014560536d9e)

**Cyfrin:** Verified. `QuantAMMBaseAdministration` is removed.

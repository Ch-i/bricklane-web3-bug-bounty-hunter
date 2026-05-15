---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-19-cyfrin-stakepet-3-5
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-09-19T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-stakepet.md
tags:
- firm:cyfrin
- report:2023-09-19-cyfrin-stakepet
title: Use != 0 instead of > 0 for unsigned integer comparison
vuln_class: []
---

# Use != 0 instead of > 0 for unsigned integer comparison

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-19-cyfrin-stakepet.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-19-cyfrin-stakepet.md)_

---

```solidity
File: StakePet.sol

269:         if (_amount > 0) {

299:         if (!petAlive && pet.ownership > 0) {

432:         if (totYield > 0) {

497:             if (_milkAmount > 0) {

541:         if (yieldToWithdraw > 0) {

558:                 require(yieldToWithdraw > 0); // This should never be hit and is maybe not needed, but just in case.

562:                 require(yieldToWithdraw > 0); // This should never be hit and is maybe not needed, but just in case.

709:         if (_totalYieldNoMilk > 0) {

723:         if (s_totalOwnership > 0) {

741:         if (s_totalOwnership > 0) {

```

```solidity
File: StakePetManager.sol

129:             if (!stakePetContract.alive(pet.lastProofOfLife) && pet.ownership > 0) {

```

**Client:** Fixed in [9e3d0d0](https://github.com/Ranama/StakePet/commit/9e3d0d0c1b6a324e22e0e3f70453c6d411cd9101)

**Cyfrin:** Verified.

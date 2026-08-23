---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-25-planar-finance-0-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-03-25T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md
tags:
- firm:zokyo
- report:2024-03-25-planar-finance
title: '`updateBeneficiary` function lacks critical validation checks'
vuln_class: []
---

# `updateBeneficiary` function lacks critical validation checks

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-03-25-Planar Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md)_

---

**Severity**: Medium

**Status**:  Unresolved

**Source**: ./libraries/VestingWallet.sol , ./libraries/VestingWallet2.sol

**Description**:

The `updateBeneficiary` function in the `VestingWallet` contract allows the contract owner to update the share of a beneficiary. However, this function lacks several critical validations that are necessary to ensure the integrity and security of the contract's operations. Specifically, the function does not validate:


- The contract has not been bootstrapped (if applicable to the contract's logic).
- The new share amount is different from the current share amount for the beneficiary.
- The beneficiary has not performed certain actions that should lock their share from being updated (e.g., transferring USD in some contexts).
- The new share amount is greater than zero.
- The beneficiary has been previously added and is not being set for the first time through this function.

**Recommendation:**

```solidity
function updateBeneficiary(address wallet, uint256 newShare) external onlyOwner {
  
  // Assuming `bootstrapped` is a state variable indicating if the contract has been bootstrapped
  require(!bootstrapped, 'Cannot update beneficiary as contract has been bootstrapped');
  require(beneficiariesShare[wallet] != newShare, 'New share cannot be the same as old share');
  // Assuming there's a way to check if a beneficiary has transferred USD or any similar condition
  require(!hasTransferredUSD[wallet], 'Beneficiary should have not transferred USD');
  require(newShare > 0, 'Share cannot be smaller or equal to 0');
  require(beneficiariesShare[wallet] != 0 || _beneficiariesWallet.contains(wallet), 'Beneficiary has not been added');

  _release();

  totalShare = totalShare.sub(beneficiariesShare[wallet]).add(newShare);
  require(totalShare <= MAX_TOTAL_SHARE, "Allocation too high");
  beneficiariesShare[wallet] = newShare;
  if (newShare == 0) _beneficiariesWallet.remove(wallet);
  else _beneficiariesWallet.add(wallet);
}
```

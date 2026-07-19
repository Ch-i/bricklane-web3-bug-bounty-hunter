---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-19-cyfrin-lido-earn-v2-0-2-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-12-19T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-19-cyfrin-lido-earn-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-19-cyfrin-lido-earn-v2-0
title: Use more efficient method of reading recipient account and basis points
vuln_class: []
---

# Use more efficient method of reading recipient account and basis points

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-19-cyfrin-lido-earn-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-19-cyfrin-lido-earn-v2.0.md)_

---

**Description:** In `RewardsDistributor::getRecipient` reduce gas cost 791 -> 716 by:
```solidity
function getRecipient(uint256 index) external view returns (address account, uint256 basisPoints) {
    Recipient storage recipient = recipients[index];
    (account, basisPoints) = (recipient.account, recipient.basisPoints);
}
```

In `RewardsDistributor::distribute` reduce gas costs 59254 -> 59172 by:
```solidity
for (uint256 i = 0; i < recipientsLength; i++) {
    Recipient storage recipient = recipients[i];
    (address account, uint256 basisPoints) = (recipient.account, recipient.basisPoints);

    uint256 amount = (balance * basisPoints) / MAX_BASIS_POINTS;

    if (amount > 0) {
        tokenContract.safeTransfer(account, amount);
        emit RecipientPaid(account, token, amount);
    }

    totalAmount += amount;
}
```

**Proof of Concept:** To verify in `RewardDistributor.t.sol`:
1) In function `test_ReplaceRecipient_Succeeds` add snapshot after last call:
```diff
function test_ReplaceRecipient_Succeeds() public {
    RewardDistributor distributor = _deployDefaultDistributor();
    address newRecipient = makeAddr("newRecipient");

    (address oldRecipient,) = distributor.getRecipient(0);

    vm.expectEmit(true, true, true, true);
    emit RewardDistributor.RecipientReplaced(0, oldRecipient, newRecipient);

    vm.prank(admin);
    distributor.replaceRecipient(0, newRecipient);

    (address updatedRecipient,) = distributor.getRecipient(0);
+   vm.snapshotGasLastCall("RewardsDistributor", "getRecipient");
    assertEq(updatedRecipient, newRecipient);
}
```

2) In function `test_Distribute_DistributesAccordingToBps` add snapshot after first call:
```diff
function test_Distribute_DistributesAccordingToBps() public {
    RewardDistributor distributor = _deployDefaultDistributor();
    uint256 amount = 10_000e6;
    asset.mint(address(distributor), amount);

    address[] memory recipients = new address[](2);
    recipients[0] = recipientA;
    recipients[1] = recipientB;

    uint256[] memory expectedAmounts = new uint256[](2);
    expectedAmounts[0] = (amount * 4_000) / MAX_BPS;
    expectedAmounts[1] = (amount * 6_000) / MAX_BPS;

    vm.recordLogs();
    vm.prank(admin);
    distributor.distribute(address(asset));
+   vm.snapshotGasLastCall("RewardsDistributor", "distribute");

    Vm.Log[] memory entries = vm.getRecordedLogs();
    // snip remaining code...
```

3) Run the test contract: `forge test --match-contract RewardDistributorTest`

4) Examine the gas snapshots: `more snapshots/RewardsDistributor.json`

5) After making the recommended changes, execute 3) and 4) again

**Lido:** Fixed in commit [4898c26](https://github.com/lidofinance/defi-interface/commit/4898c26cd0abc8426ad9e2220a8d7cac487ab9b8).

**Cyfrin:** Verified.

\clearpage

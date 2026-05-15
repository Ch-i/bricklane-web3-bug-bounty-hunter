---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-15-cyfrin-veefriends-v2-0-0-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-15T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-15-cyfrin-veefriends-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-15-cyfrin-veefriends-v2-0
title: Total supply and balance invariants can be broken by burning the same token
  id multiple times within a given batch operation
vuln_class: []
---

# Total supply and balance invariants can be broken by burning the same token id multiple times within a given batch operation

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-15-cyfrin-veefriends-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-15-cyfrin-veefriends-v2.0.md)_

---

**Description:** The `_burnBatch(uint256[])` function loops over all provided `tokenIds` and updates the relevant state; however, the ownership/approval logic is executed for all tokens in `_burnBatch(address,uint256[],bool)` before any state updates have occurred. As such, this fails to explicitly consider the scenario in which `DEAD_ADDRESS` is already the owner of a given `tokenId` if it is specified multiple times within the array and thus has been burned.

Due to the presence of an unchecked block in `totalSupply()`, the `burnCounter` can be increased arbitrarily by calling `burnBatch()` with multiple identical ids which can ultimately break the total supply invariant via underflow:

```solidity
function totalSupply() public view returns (uint256) {
    unchecked {
        return _mintCounter - _burnCounter;
    }
}
```

This occurs because burning performs a transfer from the current owner address to the `DEAD_ADDRESS`, but only validates ownership at the beginning of execution. Instead, this logic should be executed for each id in the batch in turn after the approval/ownership/balance state from the previously burned token are updated. Since the ownership is updated to the `DEAD_ADDRESS` after the first loop iteration, subsequent executions perform transfers from the `DEAD_ADDRESS` to itself which also underflows when decrementing the balance despite the following assumption:

```solidity
unchecked {
    // Cannot overflow, as that would require more tokens to be burned/transferred
    // out than the owner initially received through minting and transferring in.
    _balances[owner] -= 1;
}
```

**Impact:** The total supply and balance invariants are broken by batch burning the same token id multiple times.

**Proof of Concept:** The following test should be added to `VFTokenC.test.ts`:

```typescript
it("burning non-existent tokens", async function () {
  const { vfTokenC, owner } = await connection.networkHelpers.loadFixture(
    fixtureWithMintedTokensForBurning
  );

  await vfTokenC.connect(owner).toggleBurnActive();

  const balanceBefore = await vfTokenC.balanceOf(owner.address);
  const deadBefore = await vfTokenC.balanceOf(DEAD_ADDRESS);
  const totalSupplyBefore = await vfTokenC.totalSupply();

  await expect(vfTokenC.connect(owner).burnBatchAdmin([102, 102, 102, 102]))
    .to.emit(vfTokenC, "Transfer")
    .withArgs(owner.address, DEAD_ADDRESS, 102);

  const balanceAfter = await vfTokenC.balanceOf(owner.address);
  const deadAfter = await vfTokenC.balanceOf(DEAD_ADDRESS);
  const totalSupplyAfter = await vfTokenC.totalSupply();

  console.log("Balance before:", balanceBefore.toString());
  console.log("Balance after:", balanceAfter.toString());

  console.log("Dead before:", deadBefore.toString());
  console.log("Dead after:", deadAfter.toString());

  console.log("Total Supply before:", totalSupplyBefore.toString());
  console.log("Total Supply after:", totalSupplyAfter.toString());

  // Tokens should now be owned by DEAD_ADDRESS
  expect(await vfTokenC.ownerOf(102)).to.equal(DEAD_ADDRESS);

  // Owner balance should have decreased by one
  expect(balanceAfter).to.equal(balanceBefore - 1n);

  // Total supply should have only decreased by one (violated)
  expect(totalSupplyAfter).to.equal(totalSupplyBefore - 1n);

  // DEAD_ADDRESS balance should have increased by one (violated)
  expect(deadAfter).to.equal(deadBefore + 1n);
});
```

**Recommended Mitigation:** Consider preventing duplicate ids in the array and/or validating ownership for each id in turn after each loop iteration rather than batching before any state updates have occurred.

**VeeFriends:** Fixed in commit [dc834fa](https://github.com/veefriends/smart-contracts-v2/commit/dc834fad574e9f7caf460ba5eae2983f8d0e4488).

**Cyfrin:** Verified. Execution will now revert if the owner is already the dead address.

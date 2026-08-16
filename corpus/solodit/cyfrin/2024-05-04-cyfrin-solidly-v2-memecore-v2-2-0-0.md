---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-04-cyfrin-solidly-v2-memecore-v2-2-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-05-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md
tags:
- firm:cyfrin
- report:2024-05-04-cyfrin-solidly-v2-memecore-v2-2
title: Locks can be created with expiry in the past
vuln_class: []
---

# Locks can be created with expiry in the past

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md)_

---

**Description:** Due to a silent overflow in [`SolidityV2ERC42069::lockToken`](https://github.com/SolidlyLabs/v2-core/blob/757b18ad05780d2af22018b0c2c9d59422dc59d3/contracts/SolidlyV2-memecore.sol#L387), a sufficiently large duration will cause the unlock date to be in the past. This could allow the caller to create a fraudulent lock, advertising that they have locked for the maximum duration but which can actually be withdrawn immediately. However, the impact is somewhat limited as this will be visible to anyone who calls [`SolidityV2ERC42069::getLock(s)`](https://github.com/SolidlyLabs/v2-core/blob/757b18ad05780d2af22018b0c2c9d59422dc59d3/contracts/SolidlyV2-memecore.sol#L459-L471) with the owner's address (perhaps in a UI). From the attacker's perspective, the extension functionality could ideally be used to wrap around at will, hiding this malicious intent; however, this is not possible due to the checked math revert when incrementing the date.

**Impact:** This bug has a high likelihood of being abused with a more limited impact; therefore, it is categorized as a medium-severity finding.

**Proof of Concept:** Append this test to `MultiTest.js`:
```javascript
it("lock can be created in the past", async function () {
  const { user1, test0, test1, router, pair } = await loadFixture(deploySolidlyV2Fixture);

  let token0 = test0;
  let token1 = test1;

  // Approve tokens for liquidity provision
  await token0.connect(user1).approve(router.address, ethers.constants.MaxUint256);
  await token1.connect(user1).approve(router.address, ethers.constants.MaxUint256);

  // Provide liquidity
  await router.connect(user1).addLiquidity(
    token0.address,
    token1.address,
    ethers.utils.parseUnits("100", 18),
    ethers.utils.parseUnits("100", 18),
    0,
    0,
    user1.address,
    ethers.constants.MaxUint256
  );

  const liquidityBalance = await pair.balanceOf(user1.address);

  let blockTimestamp = (await ethers.provider.getBlock('latest')).timestamp;

  let maxUint128 = ethers.BigNumber.from("340282366920938463463374607431768211455");

  // Lock LP tokens
  await pair.connect(user1).lockToken(user1.address, liquidityBalance, maxUint128.sub(blockTimestamp));


  let ret = await pair.getLock(user1.address, 0);
  expect(ret.date).to.be.eq(0);
});
  ```
**Recommended Mitigation:** Cast the timestamp to `uint128` prior to performing the addition rather than unsafely downcasting the result of the addition:

```diff
locks[from].push(LockData({
    amount: uint128(amount - fee),
-     date: uint128(block.timestamp + duration)
+     date: uint128(block.timestamp) + duration
}));
```

**Solidly Labs:** Fixed in commit [14533e7](https://github.com/SolidlyLabs/v2-core/tree/14533e758f42009ca1d2cf4e98e2e7f33bcd4538).

**Cyfrin:** Verified. The timestamp is first cast to `uint128` prior to performing the addition.

\clearpage

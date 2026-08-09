---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-1-9
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-02-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
tags:
- firm:cyfrin
- report:2024-02-23-cyfrin-swell-barracuda
title: Repricing with small rewards results in an invalid state where `ETH` reserves
  increase, `swETH to ETH` exchange rate increases, but no rewards are paid out to
  operators or treasury
vuln_class: []
---

# Repricing with small rewards results in an invalid state where `ETH` reserves increase, `swETH to ETH` exchange rate increases, but no rewards are paid out to operators or treasury

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-02-23-cyfrin-swell-barracuda.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md)_

---

**Description:** Invariant fuzzing used repricings with small rewards to reach an invalid state where `ETH` reserves increase, `swETH : ETH` exchange rate increases, but no rewards are paid out to operators or treasury.

**Proof of Concept:** During repricing:
1) there is no minimum value enforced by either `RepricingOracle` for [`_snapshot.rewardsPayableForFees`](https://github.com/SwellNetwork/v3-contracts-lst/blob/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/RepricingOracle.sol#L227) or `swETH::reprice` for `_newETHRewards`
2) in `swETH::reprice` there is no check for rounding down to zero precision loss when [calculating](https://github.com/SwellNetwork/v3-contracts-lst/blob/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/swETH.sol#L239-L241) `rewardsInSwETH`

This results in the fuzzer reaching an invalid state where:
1) by calling `RepricingOracle::submitSnapshotV2` with small values for `_snapshot.rewardsPayableForFees`, this results in `swETH::reprice` being called with small `_newETHRewards`
2) inside `swETH::reprice` the small `_newETHRewards` triggers a rounding down to zero precision loss in the rewards calculation of `rewardsInSwETH` so [rewards are never distributed](https://github.com/SwellNetwork/v3-contracts-lst/blob/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/swETH.sol#L278)
3) however `swETH::reprice` does [update](https://github.com/SwellNetwork/v3-contracts-lst/blob/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/swETH.sol#L337) `lastRepriceETHReserves` using the small positive `_newETHRewards` value and the transaction completes successfully.

This results in an invalid state where:

1) `swETH::lastRepriceETHReserves` increases
2) `swETH : ETH` exchange rate increases
3) no rewards are being paid out to operators/treasury

This simplified PoC can be added to `reprice.test.ts`:
```typescript
    it("audit small rewards not distributed while reserves and exchange rate increasing", async () => {
      const swellTreasuryRewardPercentage = parseEther("0.1");

      await swETH_Deployer.setSwellTreasuryRewardPercentage(
        swellTreasuryRewardPercentage
      );

      await swETH_Deployer.deposit({
        value: parseEther("1000"),
      });
      const preRewardETHReserves = parseEther("1100");

      const swETHSupply = parseEther("1000");

      const ethRewards = parseUnits("1", "wei");

      const swellTreasuryPre = await swETH_Deployer.balanceOf(SwellTreasury.address);
      const ethReservesPre = await swETH_Deployer.lastRepriceETHReserves();
      const rateBefore = await swETH_Deployer.swETHToETHRate();

      swETH_Bot.reprice(
          preRewardETHReserves,
          ethRewards,
          swETH_Deployer.totalSupply());

      const swellTreasuryPost = await swETH_Deployer.balanceOf(SwellTreasury.address);
      const ethReservesPost = await swETH_Deployer.lastRepriceETHReserves();
      const rateAfter = await swETH_Deployer.swETHToETHRate();

      // no rewards distributed to treasury
      expect(swellTreasuryPre).eq(swellTreasuryPost);

      // exchange rate increases
      expect(rateBefore).lt(rateAfter);

      // reserves increase
      expect(ethReservesPre).lt(ethReservesPost);

      // repricing using small `_newETHRewards` can lead to increasing reserves
      // and increasing exchange rate without reward payouts
    });
```

This was not introduced in the new changes but is present in the current mainnet code [[1](https://github.com/SwellNetwork/v3-core-public/blob/master/contracts/lst/contracts/implementations/swETH.sol#L264), [2](https://github.com/SwellNetwork/v3-core-public/blob/master/contracts/lst/contracts/implementations/swETH.sol#L323-L325)].

**Swell:** Acknowledged.

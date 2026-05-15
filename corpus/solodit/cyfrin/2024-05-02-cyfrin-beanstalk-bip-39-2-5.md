---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-02-cyfrin-beanstalk-bip-39-2-5
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-05-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md
tags:
- firm:cyfrin
- report:2024-05-02-cyfrin-beanstalk-bip-39
title: Stalk rewards don't get burned for large partial withdrawals due to unsafe
  downcast
vuln_class: []
---

# Stalk rewards don't get burned for large partial withdrawals due to unsafe downcast

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-02-cyfrin-beanstalk-bip-39.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md)_

---

**Description:** When calling `SiloFacet::withdrawDeposit`, it is possible that Stalk rewards are not burned for large partial withdrawals as `LibSilo::stalkReward` will return 0 due to an [unsafe downcast](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/Silo/LibSilo.sol#L631-L636) of `removedBDV` from `uint128 -> int96`.

**Impact:** Stalk rewards don't get burned for large partial withdrawals.

**Proof of Concept:** Add to `SiloToken.test.js` under the section `describe("deposit", function () {`:
```javascript
    describe("audit withdrawing deposited asset for large BDV value", function () {
      // values found via fuzz testing
      let beanDeposit       = "79228162514264337593543950337";
      let problemRemovedBdv = "79228162514264337593543950336";

      beforeEach(async function () {
        await this.season.teleportSunrise(10);
        this.season.deployStemsUpgrade();

        await this.siloToken.connect(user).approve(this.silo.address, beanDeposit);
        await this.siloToken.mint(userAddress, beanDeposit);
        await this.silo.connect(user).deposit(this.siloToken.address, beanDeposit, EXTERNAL);
      });

      it("audit stalk rewards not burned when withdrawing deposited asset for large BDV value", async function () {
        let initialTotalStalk = beanDeposit + "0000";

        // verify initial state
        expect(await this.silo.getTotalDeposited(this.siloToken.address)).to.eq(beanDeposit);
        // siloToken has 1:1 BDV calc
        expect(await this.silo.getTotalDepositedBdv(this.siloToken.address)).to.eq(beanDeposit);
        expect(await this.silo.totalStalk()).to.eq(initialTotalStalk);

        // fast forward to build up some stalk rewards
        await this.season.teleportSunrise(20);

        // snapshot EVM state as we want to restore it after testing the normal
        // case works as expected
        let snapshotId = await network.provider.send("evm_snapshot");

        // normal case: withdraw the entire deposited amount
        const stem = await this.silo.seasonToStem(this.siloToken.address, "10");
        await this.silo.connect(user).withdrawDeposit(this.siloToken.address, stem, beanDeposit, EXTERNAL);

        // verify token.totalDeposited == 0
        expect(await this.silo.getTotalDeposited(this.siloToken.address)).to.eq("0");
        // verify token.totalDepositedBDV == 0
        expect(await this.silo.getTotalDepositedBdv(this.siloToken.address)).to.eq("0");
        // verify totalStalk == 0; both the initial stalk & stalk rewards were burned
        expect(await this.silo.totalStalk()).to.eq("0");

        // restore EVM state to snapshot prior to testing normal case
        await network.provider.send("evm_revert", [snapshotId]);

        // re-verify initial state
        expect(await this.silo.getTotalDeposited(this.siloToken.address)).to.eq(beanDeposit);
        // siloToken has 1:1 BDV calc
        expect(await this.silo.getTotalDepositedBdv(this.siloToken.address)).to.eq(beanDeposit);
        expect(await this.silo.totalStalk()).to.eq(initialTotalStalk);

        // problem case: partial withdraw a precise amount causing
        // by LibTokenSilo::removeDepositFromAccount() to calculate & return
        // `removedBDV` to a known exploitable value. This causes LibSilo::stalkReward()
        // to return 0 due to an unsafe downcast of `removedBDV` from uint128 -> int96
        // meaning stalk rewards are not burned when the withdrawal occurs
        await this.silo.connect(user).withdrawDeposit(this.siloToken.address, stem, problemRemovedBdv, EXTERNAL);

        // verify token.totalDeposited has been correcly decremented
        expect(await this.silo.getTotalDeposited(this.siloToken.address)).to.eq("1");
        // verify token.totalDepositedBDV == 1 as siloToken has 1:1 BDV calc
        expect(await this.silo.getTotalDepositedBdv(this.siloToken.address)).to.eq("1");

        // verify totalStalk == 10000 which fails and instead 10010 is returned.
        //
        // A return of 10010 is incorrect as there is only 1 BEAN left deposited
        // so totalStalk should equal 10000 as the 10 stalk rewards should have
        // been burned with the withdrawal, but this didn't happen due to the
        // unsafe downcast in LibSilo::stalkReward() causing stalkReward() to
        // return 0
        expect(await this.silo.totalStalk()).to.eq("10000");
      });
    });
```

**Recommended Mitigation:** The withdrawal should revert if the result of the downcast overflows such that no Stalk is burned. This could be achieved by performing a safe downcast and/or validating that a non-zero Stalk amount is burned when withdrawing a non-zero BDV. [`LibTokenSilo::toInt96`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/Silo/LibTokenSilo.sol#L478-L481) is used in that contract for validating inputs and casting.

\clearpage

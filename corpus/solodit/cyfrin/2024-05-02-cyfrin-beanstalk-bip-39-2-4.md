---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-02-cyfrin-beanstalk-bip-39-2-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-05-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md
tags:
- firm:cyfrin
- report:2024-05-02-cyfrin-beanstalk-bip-39
title: Small unripe token withdrawals don't decrease BDV and Stalk
vuln_class: []
---

# Small unripe token withdrawals don't decrease BDV and Stalk

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-02-cyfrin-beanstalk-bip-39.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md)_

---

**Description:** For any whitelisted token where `bdvCalc(amountDeposited) < amountDeposited`, a user can deposit that token and then withdraw in small amounts to avoid decreasing BDV and Stalk. This is achieved by exploiting a rounding down to zero precision loss in [`LibTokenSilo::removeDepositFromAccount`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/Silo/LibTokenSilo.sol#L248):

```solidity
// @audit small unripe bean withdrawals don't decrease BDV and Stalk
// due to rounding down to zero precision loss. Every token where
// `bdvCalc(amountDeposited) < amountDeposited` is vulnerable
uint256 removedBDV = amount.mul(crateBDV).div(crateAmount);
```

**Impact:** An attacker can withdraw deposited assets without decreasing BDV and Stalk. While the cost to perform this attack is likely more than the value an attacker would stand to gain, the potential impact should definitely be explored more closely especially considering the introduction of the Unripe Chop Convert in BIP-39 as this could have other unintended consequences in relation to this bug (given that the inflated BDV of an Unripe Token will persist once deposit is converted to its ripe counterpart, potentially allowing value to be extracted that way depending on how this BDV is used/manipulated elsewhere).

The other primary consideration for this bug is that it breaks the mechanism that Stalk is supposed to be lost when withdrawing deposited assets and keeps the `totalDepositedBdv` artificially high, violating the invariant that the `totalDepositedBdv` value for a token should be the sum of the BDV value of all the individual deposits.

**Proof of Concept:** Add this PoC to `SiloToken.test.js` under the section `describe("1 deposit, some", async function () {`:

```javascript
it('audit small unripe bean withdrawals dont decrease BDV and Stalks', async function () {
    let initialUnripeBeanDeposited    = to6('10');
    let initialUnripeBeanDepositedBdv = '2355646';
    let initialTotalStalk = pruneToStalk(initialUnripeBeanDeposited).add(toStalk('0.5'));

    // verify initial state
    expect(await this.silo.getTotalDeposited(UNRIPE_BEAN)).to.eq(initialUnripeBeanDeposited);
    expect(await this.silo.getTotalDepositedBdv(UNRIPE_BEAN)).to.eq(initialUnripeBeanDepositedBdv);
    expect(await this.silo.totalStalk()).to.eq(initialTotalStalk);

    // snapshot EVM state as we want to restore it after testing the normal
    // case works as expected
    let snapshotId = await network.provider.send('evm_snapshot');

    // normal case: withdrawing total UNRIPE_BEAN correctly decreases BDV & removes stalks
    const stem = await this.silo.seasonToStem(UNRIPE_BEAN, '10');
    await this.silo.connect(user).withdrawDeposit(UNRIPE_BEAN, stem, initialUnripeBeanDeposited, EXTERNAL);

    // verify UNRIPE_BEAN totalDeposited == 0
    expect(await this.silo.getTotalDeposited(UNRIPE_BEAN)).to.eq('0');
    // verify UNRIPE_BEAN totalDepositedBDV == 0
    expect(await this.silo.getTotalDepositedBdv(UNRIPE_BEAN)).to.eq('0');
    // verify silo.totalStalk() == 0
    expect(await this.silo.totalStalk()).to.eq('0');

    // restore EVM state to snapshot prior to testing normal case
    await network.provider.send("evm_revert", [snapshotId]);

    // re-verify initial state
    expect(await this.silo.getTotalDeposited(UNRIPE_BEAN)).to.eq(initialUnripeBeanDeposited);
    expect(await this.silo.getTotalDepositedBdv(UNRIPE_BEAN)).to.eq(initialUnripeBeanDepositedBdv);
    expect(await this.silo.totalStalk()).to.eq(initialTotalStalk);

    // attacker case: withdrawing small amounts of UNRIPE_BEAN doesn't decrease
    // BDV and doesn't remove stalks. This lets an attacker withdraw their deposits
    // without losing Stalks & breaks the invariant that the totalDepositedBDV should
    // equal the sum of the BDV of all individual deposits
    let smallWithdrawAmount = '4';
    await this.silo.connect(user).withdrawDeposit(UNRIPE_BEAN, stem, smallWithdrawAmount, EXTERNAL);

    // verify UNRIPE_BEAN totalDeposited has been correctly decreased
    expect(await this.silo.getTotalDeposited(UNRIPE_BEAN)).to.eq(initialUnripeBeanDeposited.sub(smallWithdrawAmount));
    // verify UNRIPE_BEAN totalDepositedBDV remains unchanged!
    expect(await this.silo.getTotalDepositedBdv(UNRIPE_BEAN)).to.eq(initialUnripeBeanDepositedBdv);
    // verify silo.totalStalk() remains unchanged!
    expect(await this.silo.totalStalk()).to.eq(initialTotalStalk);
});
```
Run with: `npx hardhat test --grep "audit small unripe bean withdrawals dont decrease BDV and Stalks"`.

Additional Mainnet fork tests have been written to demonstrate the presence of this bug in the current and post-BIP-39 deployments of Beanstalk (see Appendix B).

**Recommended Mitigation:** `LibTokenSilo::removeDepositFromAccount` should revert if `removedBDV == 0`. A similar check already exists in [`LibTokenSilo::depositWithBDV`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/Silo/LibTokenSilo.sol#L141) but is missing in `removeDepositFromAccount()` when calculating `removedBDV` for partial withdrawals.

The breaking of protocol invariants could lead to other serious issues that have not yet been identified but may well exist if core properties do not hold. We would urge the team to consider fixing this bug as soon as possible, prior to or as part of the BIP-39 upgrade.

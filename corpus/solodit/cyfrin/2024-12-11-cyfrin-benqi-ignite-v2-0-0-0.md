---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-0-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-12-11T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-11-cyfrin-benqi-ignite-v2-0
title: Zeeve admin could drain `ValidatorRewarder` by abusing off-chain BLS validation
  due to `QI` rewards being granted to failed registrations
vuln_class: []
---

# Zeeve admin could drain `ValidatorRewarder` by abusing off-chain BLS validation due to `QI` rewards being granted to failed registrations

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** [`Ignite::releaseLockedTokens`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L580-L583) takes the [`failed`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L578) boolean as a parameter, intended to indicate that registration of the node has failed and allow the user's stake to be recovered by a call to [`Ignite::redeemAfterExpiry`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L407). Registrations made by [`Ignite::registerWithAvaxFee`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L251) and [`Ignite::registerWithErc20Fee`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L281) are handled within the [first conditional branch](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L416-L419); however, those made via [`Ignite::registerWithStake`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L202) and [`Ignite::registerWithPrevalidatedQiStake`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L361) are not considered until the [final conditional branch](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L459-L471) shown below:

```solidity
} else {
    avaxRedemptionAmount = avaxDepositAmount + registration.rewardAmount;
    qiRedemptionAmount = qiDepositAmount;

    if (qiRewardEligibilityByNodeId[nodeId]) {
        qiRedemptionAmount += validatorRewarder.claimRewards(
            registration.validationDuration,
            registration.tokenDeposits.tokenAmount
        );
    }

    minimumContractBalance -= avaxRedemptionAmount;
}
```

This is fine for registrations made with `AVAX` stake, since the reward amount is never updated from `0`; however, for those made with pre-validated QI stake, the call to `ValidatorRewarder::claimRewards` is executed regardless, returning the original stake in QI plus QI rewards for the full duration.

Furthermore, this behavior could be abused by the Zeeve admin to drain `QI` tokens from the `ValidatorRewarder` contract. Assuming interactions are made directly with the deployed contracts to bypass frontend checks, a faulty BLS proof can be provided to `StakingContract::registerNode` – this BLS proof is validated by an off-chain service when the `NewRegistration` event is detected, and `Ignite::releaseLockedTokens` will be called if it is invalid.

While Zeeve is somewhat of a trusted entity, they could very easily and relatively inconspicuously stake with burner user addresses, forcing the failure of BLS proof validation to drain the `ValidatorRewarder` contract due to the behavior of this off-chain logic in conjunction with the incorrect handling of `QI` rewards for failed registrations.

**Impact:** `QI` rewards will be paid to users of failed registrations made via `Ignite::registerWithPrevalidatedQiStake`. If abused by the Zeeve admin, then entire `ValidatorRewarder` contract balance could be drained.

**Proof of Concept:** The following test can be added to `Ignite.test.js` under `describe("Superpools")`:

```javascript
it("earns qi rewards for failed registrations", async function () {
  await validatorRewarder.setTargetApr(1000);
  await ignite.setValidatorRewarder(validatorRewarder.address);
  await grantRole("ROLE_RELEASE_LOCKED_TOKENS", admin.address);

  // AVAX $20, QI $0.01
  const qiStake = hre.ethers.utils.parseEther("200").mul(2_000);
  const qiFee = hre.ethers.utils.parseEther("1").mul(2_000);

  // approve Ignite to spend pre-validated QI (bypassing StakingContract)
  await qi.approve(ignite.address, qiStake.add(qiFee));
  await ignite.registerWithPrevalidatedQiStake(
    admin.address,
    "NodeID-Superpools1",
    "0x" + blsPoP.toString("hex"),
    86400 * 28,
    qiStake.add(qiFee),
  );

  // registration of node fails
  await ignite.releaseLockedTokens("NodeID-Superpools1", true);

  const balanceBefore = await qi.balanceOf(admin.address);
  await ignite.connect(admin).redeemAfterExpiry("NodeID-Superpools1");

  const balanceAfter = await qi.balanceOf(admin.address);

  // stake + rewards are returned to the user
  expect(Number(balanceAfter.sub(balanceBefore))).to.be.greaterThan(Number(qiStake));
});
```

**Recommended Mitigation:** Avoid paying QI rewards to failed registrations by resetting the `qiRewardEligibilityByNodeId` state in `Ignite::releaseLockedTokens`:

```diff
    } else {
        minimumContractBalance += msg.value;
        totalSubsidisedAmount -= 2000e18 - msg.value;
+       qiRewardEligibilityByNodeId[nodeId] = false;
    }
```

**BENQI:** Fixed in commit [0255923](https://github.com/Benqi-fi/ignite-contracts/pull/16/commits/0255923e9c0d23c3fde71a6bdf1237ec4677c02d).

**Cyfrin:** Verified, `QI` rewards are no longer granted to failed registrations.

\clearpage

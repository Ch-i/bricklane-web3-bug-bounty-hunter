---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-dolomite-polvaults-v2-0-2-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-dolomite-POLVaults-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-dolomite-polvaults-v2-0
title: Rewards in iBGT cannot be redeemed when infrared vault staking is paused
vuln_class: []
---

# Rewards in iBGT cannot be redeemed when infrared vault staking is paused

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-dolomite-POLVaults-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-dolomite-POLVaults-v2.0.md)_

---

**Description:** Current reward handling mechanism enforces automatic reinvestment of iBGT rewards back into the staking pool, without providing an alternative when staking is disabled.

When the Infrared protocol pauses staking (which can happen for various reasons such as security emergencies or technical issues), users are left with no way to access their earned rewards, effectively freezing these assets until staking is resumed. It is noteworthy that [InfraredVault](https://berascan.com/address/0x67b4e6721ad3a99b7ff3679caee971b07fd85cd1#code) does not prevent redeeming rewards/ unstaking even when staking is paused

The issue lies in the `_handleRewards` function, which automatically attempts to reinvest iBGT rewards:

```solidity
function _handleRewards(IInfraredVault.UserReward[] memory _rewards) internal {
    IIsolationModeVaultFactory factory = IIsolationModeVaultFactory(VAULT_FACTORY());
    for (uint256 i = 0; i < _rewards.length; ++i) {
        if (_rewards[i].amount > 0) {
            if (_rewards[i].token == UNDERLYING_TOKEN()) {
                _setIsDepositSourceThisVault(true);
                factory.depositIntoDolomiteMargin(
                    DEFAULT_ACCOUNT_NUMBER,
                    _rewards[i].amount
                );
                assert(!isDepositSourceThisVault());
            } else {
                // ... handle other token types ...
            }
        }
    }
}
```

When the staking function in the Infrared vault is paused, as it can be through the pauseStaking() function...

```solidity
/// @inheritdoc IInfraredVault
function pauseStaking() external onlyInfrared {
    if (paused()) return;
    _pause();
}
```

...the staking operation in `executeDepositIntoVault` will fail due to the whenNotPaused modifier in the InfraredVault:

```solidity
function stake(uint256 amount) external whenNotPaused {
     // code
```

**Impact:** Users on Dolomite are unable to access their earned rewards during periods when staking is paused in the Infrared vault even though such redemption is allowed on Infrared vaults.


**Proof of Concept:** The `TestInfraredVault` is made `Pausable` to align with the on-chain Infrared vault contract and `whenNotPaused` modifier is added to the `stake` function.

```solidity
contract TestInfraredVault is ERC20, Pausable {

   function unpauseStaking() external {
        if (!paused()) return;
        _unpause();
    }

    function pauseStaking() external {
        if (paused()) return;
        _pause();
    }

    function stake(uint256 amount) external whenNotPaused {
        _mint(msg.sender, amount);
        IERC20(asset).transferFrom(msg.sender, address(this), amount);
    }
}
```

Add the following test to the #getReward class of tests in `InfraredBGTIsolationModeTokenVaultV1.ts`

```typescript
  it('should revert when staking is paused and rewards are in iBGT', async () => {
      await testInfraredVault.setRewardTokens([core.tokens.iBgt.address]);

      // Add iBGT as reward token and fund the reward
      await core.tokens.iBgt.connect(iBgtWhale).approve(testInfraredVault.address, rewardAmount);
      await testInfraredVault.connect(iBgtWhale).addReward(core.tokens.iBgt.address, rewardAmount);
      await registry.connect(core.governance).ownerSetIBgtStakingVault(testInfraredVault.address);

      // Deposit iBGT into the vault
      await iBgtVault.depositIntoVaultForDolomiteMargin(defaultAccountNumber, amountWei);
      await expectProtocolBalance(core, iBgtVault, defaultAccountNumber, iBgtMarketId, amountWei);

      // Advance time to accumulate rewards
      await increase(ONE_DAY_SECONDS * 30);

      // Pause staking in the InfraredVault
      await testInfraredVault.pauseStaking();
      expect(await testInfraredVault.paused()).to.be.true;

      //Calling getReward should revert because reinvesting iBGT rewards will fail due to staking being paused
      await expectThrow(
        iBgtVault.getReward()
      );


      // Verify balances remain unchanged
      await expectWalletBalance(iBgtVault, core.tokens.iBgt, ZERO_BI);
      await expectProtocolBalance(core, iBgtVault, defaultAccountNumber, iBgtMarketId, amountWei);

      // Unpause to allow normal operation to continue
      await testInfraredVault.unpauseStaking();
      expect(await testInfraredVault.paused()).to.be.false;

      // Now getReward should succeed
      await iBgtVault.getReward();
      await expectWalletBalance(iBgtVault, core.tokens.iBgt, ZERO_BI);
      await expectProtocolBalance(core, iBgtVault, defaultAccountNumber, iBgtMarketId, amountWei.add(rewardAmount));

      // Verify the reward was restaked
      expect(await testInfraredVault.balanceOf(iBgtVault.address)).to.eq(amountWei.add(rewardAmount));
    });
```


**Recommended Mitigation:** Consider checking if the BGT staking vault is `paused` before attempting to re-invest the rewards. If vault is paused, rewards can either be retained in the vault or transferred back to the vault owner.

**Dolomite:** Fixed in [7b83e77](https://github.com/dolomite-exchange/dolomite-margin-modules/commit/7b83e778d739c9afb039a8a8d4fe06d931f4bb22).

**Cyfrin:** Verified

\clearpage

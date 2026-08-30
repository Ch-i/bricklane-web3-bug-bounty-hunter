---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-1-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[H-02] `claimUnassignedAssets` is increasing debt but not checking for it
  in `_finaliseTrove`, opening up for self-liquidations'
vuln_class: []
---

# [H-02] `claimUnassignedAssets` is increasing debt but not checking for it in `_finaliseTrove`, opening up for self-liquidations

_Section severity (from Solodit section header): Medium_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact** 

`claimUnassignedAssets` will increase the amount of debt and collateral to a trove by a certain amount

Resulting in a Coll Increase and a Debt Increase

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/BorrowerOperations.sol#L614-L665

```solidity
function claimUnassignedAssets(
    uint _percentage,
    address _upperHint,
    address _lowerHint,
    bytes[] memory _priceUpdateData
  ) external payable override {
    if (_percentage == 0) revert ZeroDebtChange();
    /// @audit Self Liquidation Risk?
    address borrower = msg.sender;
    (ContractsCache memory contractsCache, LocalVariables_adjustTrove memory vars) = _prepareTroveAdjustment(
      borrower,
      _priceUpdateData,
      false
    );

    // handle debts
    DebtTokenAmount[] memory debtsToAdd = new DebtTokenAmount[](vars.priceCache.debtPrices.length);
    for (uint i = 0; i < vars.priceCache.debtPrices.length; i++) {
      address debtToken = vars.priceCache.debtPrices[i].tokenAddress;

      uint unassignedDebt = contractsCache.storagePool.getValue(debtToken, false, PoolType.Unassigned);
      if (unassignedDebt == 0) continue;

      uint toClaim = (unassignedDebt * _percentage) / DECIMAL_PRECISION;
      if (unassignedDebt == 0) continue;

      contractsCache.storagePool.transferBetweenTypes(debtToken, false, PoolType.Unassigned, PoolType.Active, toClaim);
      debtsToAdd[i] = DebtTokenAmount(IDebtToken(debtToken), toClaim, 0);
    }
    vars.newCompositeDebtInUSD += _getCompositeDebt(contractsCache.priceFeed, vars.priceCache, debtsToAdd);
    contractsCache.troveManager.increaseTroveDebt(borrower, debtsToAdd);

    // handle colls
    TokenAmount[] memory collsToAdd = new TokenAmount[](vars.priceCache.collPrices.length);
    for (uint i = 0; i < vars.priceCache.collPrices.length; i++) {
      address collToken = vars.priceCache.collPrices[i].tokenAddress;

      uint unassignedColl = contractsCache.storagePool.getValue(collToken, true, PoolType.Unassigned);
      if (unassignedColl == 0) continue;

      uint toClaim = (unassignedColl * _percentage) / DECIMAL_PRECISION;
      if (unassignedColl == 0) continue;

      contractsCache.storagePool.transferBetweenTypes(collToken, true, PoolType.Unassigned, PoolType.Active, toClaim);
      collsToAdd[i] = TokenAmount(collToken, toClaim);
    }
    vars.newCompositeCollInUSD += _getCompositeColl(contractsCache.priceFeed, vars.priceCache, collsToAdd);
    vars.newIMCR = _calculateIMCR(vars, collsToAdd, true);
    contractsCache.troveManager.increaseTroveColl(borrower, collsToAdd);

    _finaliseTrove(false, false, contractsCache, vars, borrower, _upperHint, _lowerHint);
  }
```

but it's calling ```_finaliseTrove(false, false,``` which means that these checks applied when `_isDebtIncrease == true` are going to be skipped

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/BorrowerOperations.sol#L978-L986

```solidity
    if (_vars.isInRecoveryMode) {
      // BorrowerOps: Collateral withdrawal not permitted Recovery Mode
      if (_isCollWithdrawal) revert CollWithdrawPermittedInRM();
      if (_isDebtIncrease) _requireICRisAboveCCR(_vars.newICR);
    } else {
      // if Normal Mode

      // check if the individual minimum collateral ratio is met (based on the used coll types)
      if (_isCollWithdrawal || _isDebtIncrease) _requireICRisAboveIMCR(_vars.newICR, _vars.newIMCR);
```

**Mitigation**

Change the code to

```solidity
_finaliseTrove(false, true, contractsCache, vars, borrower, _upperHint, _lowerHint);
```

### [H-03] `BorrowerOperations` Inconsistent IMCR logic could allow risky collaterals to have a higher CollerateralRatio during Recovery Mode

**Impact**

`_requireValidAdjustmentInCurrentMode` is a key part of the security checks for adjusting and opening Troves

From discussing with the team, I was made aware that some Collaterals may have a IMCR that would be above CCR (e.g. 175% CR)

Given this fact, we can check that the logic in `_requireValidAdjustmentInCurrentMode` will relax it's IMCR requirements during recovery mode:

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/BorrowerOperations.sol#L978-L986

```solidity
    if (_vars.isInRecoveryMode) {
      // BorrowerOps: Collateral withdrawal not permitted Recovery Mode
      if (_isCollWithdrawal) revert CollWithdrawPermittedInRM();
      if (_isDebtIncrease) _requireICRisAboveCCR(_vars.newICR);
    } else {
      // if Normal Mode

      // check if the individual minimum collateral ratio is met (based on the used coll types)
      if (_isCollWithdrawal || _isDebtIncrease) _requireICRisAboveIMCR(_vars.newICR, _vars.newIMCR);
```

In Normal Mode:
```solidity
 _requireICRisAboveIMCR(_vars.newICR, _vars.newIMCR);
```

e.g.
```
X > 175%
```

In Recovery Mode
```solidity
 _requireICRisAboveCCR(_vars.newICR);
```

```
X > 150%
```

Meaning that due to not additionally checking for IMCR, some borrowers will have more borrowing power in Recovery Mode

**Mitigation**

You can quickly mitigate this by:
- Enforcing that all CollateralRatios are below CCR
- Adding an additional check for IMCR in all modes, at all times

It's worth exploring whether certain collaterals could not be added during Recovery Mode as to further reduce risks, I think this would require simulating various prices for specific collaterals

### [H-04] Lack of min borrow + min fee allows Spam Opening troves to trigger Recovery Mode

**Impact**

This finding chains multiple other observations to borrow for free

Because a Trove can be opened with 0 net debt, such trove won't pay a borrow fee

By opening a myriad of Troves, with a ICR < TCR we can drag the TCR down

By choosing an oracle price that is a valid negative update (for collateral, or positive update for debt denomination), we can hurt the ICR of these position slightly

When the system is in Recovery Mode, no borrowing fee is paid on opening a position, this can help borrow more stablecoin as a means to raise the ownership percentage of attacker in the Stability Pool, making the liquidations directly profitable to them

This allows to trigger Recovery Mode at will, and liquidate any victim with ICR < TCR

**Proof of Concept**

- Setup by opening a myriad of Troves at ICR < TCR
- Update the price to trigger Recovery Mode
- Open the "real" trove a user wanted to open
- Borrow and bypass fees
- Liquidate Victims
- Close all other Troves that were opened for the setup

This can be fully automated with a smart contract that creates new proxies that open a Trove each

This could be used for 3 key reasons:
- Trigger Recovery Mode and Liquidate other people
- Borrow for free
- Raise the total amount of debt in the system to reduce the net fee on redemptions

**Mitigation**

I believe that Oracle price being non-deterministic on each block is a key issue

Additionally the fact that no minimum borrow size is enforced, means that these 0-net-debt are effectively free to open, whereas if some fee was charged that wouldn't be the case

Alternatively, you could always enforce a borrow fee at all times, this would have the downside of making liquidations less profitable and should be further researched

### [H-05] `StakingOperations` Token Transfer is updating the total supply before accruing rewards to users causing loss of rewards

**Impact**

```solidity
 function updatePool(ISwapPair _pid) public {
    PoolInfo storage pool = poolInfo[_pid];

    // check
    if (block.timestamp <= pool.lastRewardTime) return;

    // update
    uint tokenSupply = _pid.balanceOf(address(this));
    if (tokenSupply == 0 || totalAllocPoint == 0) {
      pool.lastRewardTime = block.timestamp;
      return;
    }
    uint multiplier = block.timestamp - pool.lastRewardTime;
    uint reward = (multiplier * rewardsPerSecond * pool.allocPoint) / totalAllocPoint;
    pool.accRewardPerShare += (reward * REWARD_DECIMALS) / tokenSupply;
    pool.lastRewardTime = block.timestamp;
  }
```

-> Transfer
-> New Balance
-> Check points (user uses old balance, but total supply is the new one)
-> User lost rewards
-> New total Supply and correct total debt

In fixing this be careful not to cause a division by zero (as the initial deposit would)

This can only happen on deposits (which dilute rewards), if the same mistake was done on withdrawals, then value could be stolen


**Mitigation**

Because the code is tightly coupled, I think accruing and then transferring the tokens could be sufficient

Alternatively the scalable fix is to track the previous balance in storage as you suggested

I think tracking in storage is the best fix long term (allows to re-use the contract separately without bugs)

### [H-06] `StakingOperations.claim` doesn't update reward debt, allowing multiple claims

**Impact**

```solidity
  function claim(ISwapPair _pid) external override {
    requireValidPool(_pid);
    _claim(_pid, msg.sender);
  }

  function batchClaim(ISwapPair[] memory _pids) external override {
    uint length = _pids.length;
    for (uint n = 0; n < length; n++) {
      requireValidPool(_pids[n]);
      _claim(_pids[n], msg.sender);
    }
```

User rewards are computed as `((user.amount * accRewardPerShare) / REWARD_DECIMALS) - user.rewardDebt;`

`user.rewardDebt = (user.amount * pool.accRewardPerShare) / REWARD_DECIMALS;` is set in deposit and withdraw

but it is not update on `claim` and `batchClaim`

Due to this, an exploiter can simply call `claim` and `batchClaim` repeatedly and steal all rewards

**Mitigation**

Change `_claim` to:
- Calculate user rewards and cache that value
- Set user debt to the new value, so their `pendingReward` are now zero
- Then transfer the tokens

Also consider implementing the following invariants:
- `pendingReward` are set to zero after a call to `claim` and `batchClaim`

### H-07 Pull Based Oracle opens up to triggering Recovery Mode and liquidating other Troves as a risk free arbitrage

**Executive Summary**

Pull Based oracle can be viewed as offering an attacker the ability to chose a combination of price that are not stale

This, combined with the possibility of lowering the TCR down via ones own positions opens up to a risk free arbitrage in which an attacker drags the TCR down to trigger Recovery Mode, and then they liquidate other people troves

**Description**

<img width="629" alt="Screenshot 2024-08-08 at 11 26 02" src="https://github.com/user-attachments/assets/6d3e67ef-fa98-43cc-831f-582671ca8aea">

Pyth Pull Oracles can be viewed as a sequence of prices, `p0` to `pn` where any ordered sequence `p0 -> px -> pn` can be picked as long as all prices are within the staleness threshold

Recovery Mode allows healthy Troves to be liquidated when the TCR falls below a certain threshold

Liquidations can be performed arbitrarily and out of order, as long as a Trove meets the requirements for Liquidations

Due to this, an attacker can push the TCR down very close to Recovery Mode and then update prices to a more negative price to trigger Recovery Mode, and perform liquidations.

This is a risk free opportunity that could be abused any time the threshold for profit is met:
- `Profit = Gain from Liquidation * Ownership % - Opening Fees - Gas Costs`


**Proof Of Concept**

- Wait for a price sequence that will result in a decrease of TCR
- Use the older price (healthier price)
- Flashloan funds, borrow to bring the TCR very close to Recovery Mode
- Deposit into the Stability Pool, ideally a very high amount to maximize profits
- Update Prices, Recovery Mode is triggered
- Liquidate other Troves (ideally out of order, to liquidate a higher amount of collateral)
- Attacker closes their position

**Mitigation**

A few ideas for mitigation:
- Offer a Grace Period in which Recovery Mode liquidations cannot happen, this can be a short delay (e.g. 15 minutes), which should allow victims to react (as long as they have setup monitoring and automations) - This is the safer option with the clear downside of a risk of desynching the state (as Recovery Mode may be engaged, but the timer would require an external call to be triggered)

- You could enforce a different ratio at which opening Troves can be performed, but this would limit opening CRs always above the CCR, a buffer could be gamed by setting up Troves that over time have their CR below the CCR, or by setting up a very heathy Trove and then closing it

- You may explore whether it's possible to always use the latest Pyth Price and enforce that only the latest price is used, this  main risk would be the inability to perform operations anytime a transaction was in the mempool for too long

Also note that because you have a mixture of Collaterals and Debt Tokens, the opportunity to trigger Recovery Mode is higher than if you only used a single Collateral and Debt Pair

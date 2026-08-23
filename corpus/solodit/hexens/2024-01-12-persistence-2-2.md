---
affected_contracts: []
derives_from: []
id: solodit-hexens-2024-01-12-persistence-2-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2024-01-12-Persistence.md
tags:
- firm:hexens
- report:2024-01-12-persistence
title: '[PRST-7] Total unbonding amounts can be greater than total liquid tokens in
  unstake'
vuln_class: []
---

# [PRST-7] Total unbonding amounts can be greater than total liquid tokens in unstake

_Section severity (from Solodit section header): Low_  
_Audit firm: Hexens_  
_Source report: [2024-01-12-Persistence.md](https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2024-01-12-Persistence.md)_

---

**Severity:** Low

**Path:** x/liquidstake/keeper/liquidstake.go:LiquidUnstake

**Description:**

The function LiquidUnstake allows a user to unstake by burning their shares and receiving unbondings for xprt.

The amount of xprt is calculated using the StkXPRTToNativeToken function, which takes the net asset value from GetNetAmountState. Afterwards, the amount is divided among validators based on their liquid token amounts and the total liquid token amount using DivideByCurrentWeight.

However, the net asset value calculation uses the module’s xprt balance, as well as unclaimed rewards in the total net amount, which is used to convert the user’s shares to the xprt amount. As a result, the unbondingAmount could be greater than totalLiquidTokens in the call to DivideByCurrentWeight.

In this case, too much would be unnecessarily unbonded from the validators or the execution would fail.

```func (k Keeper) LiquidUnstake(
	ctx sdk.Context, proxyAcc, liquidStaker sdk.AccAddress, unstakingStkXPRT sdk.Coin,
) (time.Time, math.Int, []stakingtypes.UnbondingDelegation, math.Int, error) {
	[..]
	// Get NetAmount states
	nas := k.GetNetAmountState(ctx)

	if unstakingStkXPRT.Amount.GT(nas.StkxprtTotalSupply) {
		return time.Time{}, sdk.ZeroInt(), []stakingtypes.UnbondingDelegation{}, sdk.ZeroInt(), types.ErrInvalidStkXPRTSupply
	}

	// UnstakeAmount = NetAmount * StkXPRTAmount/TotalSupply * (1-UnstakeFeeRate)
	unbondingAmount := types.StkXPRTToNativeToken(unstakingStkXPRT.Amount, nas.StkxprtTotalSupply, nas.NetAmount)
	unbondingAmount = types.DeductFeeRate(unbondingAmount, params.UnstakeFeeRate)
	unbondingAmountInt := unbondingAmount.TruncateInt()
	[..]
	liquidVals := k.GetAllLiquidValidators(ctx)
	totalLiquidTokens, liquidTokenMap := liquidVals.TotalLiquidTokens(ctx, k.stakingKeeper, false)
	[..]
	unbondingAmounts, crumb := types.DivideByCurrentWeight(liquidVals, unbondingAmount, totalLiquidTokens, liquidTokenMap)
	if !unbondingAmount.Sub(crumb).IsPositive() {
		return time.Time{}, sdk.ZeroInt(), []stakingtypes.UnbondingDelegation{}, sdk.ZeroInt(), types.ErrTooSmallLiquidUnstakingAmount
	}

	totalReturnAmount := sdk.ZeroInt()

	var ubdTime time.Time
	ubds := make([]stakingtypes.UnbondingDelegation, 0, len(liquidVals))
	for i, val := range liquidVals {
		// skip zero weight liquid validator
		if !unbondingAmounts[i].IsPositive() {
			continue
		}

		var ubd stakingtypes.UnbondingDelegation
		var returnAmount math.Int
		var weightedShare math.LegacyDec

		// calculate delShares from tokens with validation
		weightedShare, err = k.stakingKeeper.ValidateUnbondAmount(ctx, proxyAcc, val.GetOperator(), unbondingAmounts[i].TruncateInt())
		if err != nil {
			return time.Time{}, sdk.ZeroInt(), []stakingtypes.UnbondingDelegation{}, sdk.ZeroInt(), err
		}

		if !weightedShare.IsPositive() {
			continue
		}

		// unbond with weightedShare
		ubdTime, returnAmount, ubd, err = k.LiquidUnbond(ctx, proxyAcc, liquidStaker, val.GetOperator(), weightedShare, true)
		if err != nil {
			return time.Time{}, sdk.ZeroInt(), []stakingtypes.UnbondingDelegation{}, sdk.ZeroInt(), err
		}

		ubds = append(ubds, ubd)
		totalReturnAmount = totalReturnAmount.Add(returnAmount)
	}

	return ubdTime, totalReturnAmount, ubds, sdk.ZeroInt(), nil
}

func DivideByCurrentWeight(lvs LiquidValidators, input math.LegacyDec, totalLiquidTokens math.Int, liquidTokenMap map[string]math.Int) (outputs []math.LegacyDec, crumb math.LegacyDec) {
	if !totalLiquidTokens.IsPositive() {
		return []math.LegacyDec{}, sdk.ZeroDec()
	}

	totalOutput := sdk.ZeroDec()
	unitInput := input.QuoTruncate(math.LegacyNewDecFromInt(totalLiquidTokens))
	for _, val := range lvs {
		output := unitInput.MulTruncate(math.LegacyNewDecFromInt(liquidTokenMap[val.OperatorAddress])).TruncateDec()
		totalOutput = totalOutput.Add(output)
		outputs = append(outputs, output)
	}

	return outputs, input.Sub(totalOutput)
}

func StkXPRTToNativeToken(stkXPRTAmount, stkXPRTTotalSupplyAmount math.Int, netAmount math.LegacyDec) (nativeTokenAmount math.LegacyDec) {
	return math.LegacyNewDecFromInt(stkXPRTAmount).MulTruncate(netAmount).Quo(math.LegacyNewDecFromInt(stkXPRTTotalSupplyAmount)).TruncateDec()
}

func (k Keeper) GetNetAmountState(ctx sdk.Context) (nas types.NetAmountState) {
	totalRemainingRewards, totalDelShares, totalLiquidTokens := k.CheckDelegationStates(ctx, types.LiquidStakeProxyAcc)

	totalUnbondingBalance := sdk.ZeroInt()
	ubds := k.stakingKeeper.GetAllUnbondingDelegations(ctx, types.LiquidStakeProxyAcc)
	for _, ubd := range ubds {
		for _, entry := range ubd.Entries {
			// use Balance(slashing applied) not InitialBalance(without slashing)
			totalUnbondingBalance = totalUnbondingBalance.Add(entry.Balance)
		}
	}

	nas = types.NetAmountState{
		StkxprtTotalSupply:    k.bankKeeper.GetSupply(ctx, k.LiquidBondDenom(ctx)).Amount,
		TotalDelShares:        totalDelShares,
		TotalLiquidTokens:     totalLiquidTokens,
		TotalRemainingRewards: totalRemainingRewards,
		TotalUnbondingBalance: totalUnbondingBalance,
		ProxyAccBalance:       k.GetProxyAccBalance(ctx, types.LiquidStakeProxyAcc).Amount,
	}

	nas.NetAmount = nas.CalcNetAmount()
	nas.MintRate = nas.CalcMintRate()
	return
}
```

**Remediation:**  The LiquidUnstake function has a branch where the user receives the xprt from the module’s balance, but this only happens if the totalLiquidTokens is 0 and there is enough balance. We would recommend to have the function first use any existing balance to convert the xprt amount and use the remaining value to unbond from validators.

**Status:**  Acknowledged

- - -

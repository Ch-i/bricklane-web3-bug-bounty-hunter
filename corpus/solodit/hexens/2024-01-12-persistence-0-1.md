---
affected_contracts: []
derives_from: []
id: solodit-hexens-2024-01-12-persistence-0-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2024-01-12-Persistence.md
tags:
- firm:hexens
- report:2024-01-12-persistence
title: '[PRST-1] Division by zero in share conversion leads to panic and denial-of-service'
vuln_class: []
---

# [PRST-1] Division by zero in share conversion leads to panic and denial-of-service

_Section severity (from Solodit section header): High_  
_Audit firm: Hexens_  
_Source report: [2024-01-12-Persistence.md](https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2024-01-12-Persistence.md)_

---

**Severity:** High

**Path:** x/liquidstake/types/liquidstake.go:NativeTokenToStkXPRT, StkXPRTToNativeToken#L167-L175

**Description:**

Both functions `NativeTokenToStkXPRT` and `StkXPRTToNativeToken` are used to convert `xprt` to `stkxprt` and vice versa. The conversion is based on the total net amount of assets and the stkXPRT total supply.

However, neither function checks whether the denominator is zero, nor is this check done when either function is called.

This becomes a problem in the `keeper.LiquidStake` function when the user deposits `xprt` for `stkxprt`. Here `NativeTokenToStkXPRT` is called to calculate the amount of `stkxprt`.

If the protocol is in a state where there are some stkXPRT shares but no net assets, then a division by zero will happen. This will cause the message to revert with a Go run-time panic. This would make staking not possible.

```
// NativeTokenToStkXPRT returns StkxprtTotalSupply * nativeTokenAmount / netAmount
func NativeTokenToStkXPRT(nativeTokenAmount, stkXPRTTotalSupplyAmount math.Int, netAmount math.LegacyDec) (stkXPRTAmount math.Int) {
	return math.LegacyNewDecFromInt(stkXPRTTotalSupplyAmount).MulTruncate(math.LegacyNewDecFromInt(nativeTokenAmount)).QuoTruncate(netAmount.TruncateDec()).TruncateInt()
}

// StkXPRTToNativeToken returns stkXPRTAmount * netAmount / StkxprtTotalSupply with truncations
func StkXPRTToNativeToken(stkXPRTAmount, stkXPRTTotalSupplyAmount math.Int, netAmount math.LegacyDec) (nativeTokenAmount math.LegacyDec) {
	return math.LegacyNewDecFromInt(stkXPRTAmount).MulTruncate(netAmount).Quo(math.LegacyNewDecFromInt(stkXPRTTotalSupplyAmount)).TruncateDec()
}
```

**Remediation:**  Both functions should correctly handle the case where the denominator is zero in the same was that `MintRate` is calculated in `GetNetAmountState`.

**Status:**  Fixed

- - -

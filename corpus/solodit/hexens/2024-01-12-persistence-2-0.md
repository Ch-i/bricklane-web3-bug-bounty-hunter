---
affected_contracts: []
derives_from: []
id: solodit-hexens-2024-01-12-persistence-2-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2024-01-12-Persistence.md
tags:
- firm:hexens
- report:2024-01-12-persistence
title: '[PRST-2] Whitelisted validator target weight is uncapped and unitless'
vuln_class: []
---

# [PRST-2] Whitelisted validator target weight is uncapped and unitless

_Section severity (from Solodit section header): Low_  
_Audit firm: Hexens_  
_Source report: [2024-01-12-Persistence.md](https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2024-01-12-Persistence.md)_

---

**Severity:** Low

**Path:** x/liquidstake/types/params.go:validateWhitelistedValidators#L101-L126

**Description:**

The function `validateWhitelistedValidators` will validate a new set of whitelisted validators as proposed by Governance through the `UpdateParams` message.

However, this function only checks whether the target weight is positive, the actual value is not checked or scaled against anything.

This makes it so that a validator’s target weight by itself is meaningless, you have to compare it to the total target weight of all validators. Furthermore, the target weight is uncapped, so one validator with an enormous target weight would disable all other validators and take all power for themselves.

```func validateWhitelistedValidators(i interface{}) error { 
	wvs, ok := i.([]WhitelistedValidator)
	if !ok {
		return fmt.Errorf("invalid parameter type: %T", i)
	}
	valsMap := map[string]struct{}{}
	for _, wv := range wvs {
		_, valErr := sdk.ValAddressFromBech32(wv.ValidatorAddress)
		if valErr != nil {
			return valErr
		}

		if wv.TargetWeight.IsNil() {
			return fmt.Errorf("liquidstake validator target weight must not be nil")
		}
		if !wv.TargetWeight.IsPositive() {
			return fmt.Errorf("liquidstake validator target weight must be positive: %s", wv.TargetWeight)
		}

		if _, ok := valsMap[wv.ValidatorAddress]; ok {
			return fmt.Errorf("liquidstake validator cannot be duplicated: %s", wv.ValidatorAddress)
		}
		valsMap[wv.ValidatorAddress] = struct{}{}
	}
	return nil
}
```

**Remediation:**  We would recommend to implement some kind of cap and unit for the target weight. For example, 1 `Dec` would mean `1x` normal stake for a validator and there could be a cap of `10x` or `100x` as desired (or configurable by Governance).

**Status:** Fixed

- - -

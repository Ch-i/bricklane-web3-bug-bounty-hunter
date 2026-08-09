---
affected_contracts: []
derives_from: []
id: solodit-hexens-2024-01-12-persistence-2-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2024-01-12-Persistence.md
tags:
- firm:hexens
- report:2024-01-12-persistence
title: '[PRST-3] Whitelisted validators cannot be inactivated'
vuln_class: []
---

# [PRST-3] Whitelisted validators cannot be inactivated

_Section severity (from Solodit section header): Low_  
_Audit firm: Hexens_  
_Source report: [2024-01-12-Persistence.md](https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2024-01-12-Persistence.md)_

---

**Severity:** Low

**Path:** x/liquidstake/types/params.go:validateWhitelistedValidators#L101-L126

**Description:**

According to the documentation of a `WhitelistedValidator`, a validator is deemed inactive if their target weight is set to zero. This can be seen in `x/liquidstake/types/liquidstake.pb.go` on lines 122-125:

```
// WhitelistedValidator consists of the validator operator address and the
// target weight, which is a value for calculating the real weight to be derived
// according to the active status. In the case of inactive, it is calculated as
// zero.
```
However, this is not possible when updating the whitelisted validator set through `UpdateParams`. When it is validating the new set in `validateWhitelistedValidators` on lines 116-118:

```
if !wv.TargetWeight.IsPositive() {
	return fmt.Errorf("liquidstake validator target weight must be positive: %s", wv.TargetWeight)
}
```
The check will return an error if the target weight is `<= 0`, `isPositive` only returns true if the value is greater than zero.

```
func validateWhitelistedValidators(i interface{}) error { 
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

**Remediation:**  Either the documentation should be amended to correctly state that inactive validators would not be included in the set, or the validation code should also allow a target weight of zero.

**Status:** Fixed


- - -

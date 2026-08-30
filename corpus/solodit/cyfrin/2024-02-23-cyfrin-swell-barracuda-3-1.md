---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-3-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-02-23T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
tags:
- firm:cyfrin
- report:2024-02-23-cyfrin-swell-barracuda
title: Cache array length outside of loops and consider unchecked loop incrementing
vuln_class: []
---

# Cache array length outside of loops and consider unchecked loop incrementing

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-02-23-cyfrin-swell-barracuda.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md)_

---

**Description:** Cache array length outside of loops and consider using `unchecked {++i;}` if not compiling with `solc --ir-optimized --optimize`:

File: `DepositManager.sol`
```solidity
// @audit cache `validatorDetails.length`
116:    for (uint256 i; i < validatorDetails.length; i++) {
```

File: `NodeOperatorRegistry.sol`
```solidity
// @audit cache `numOperators`
133:    uint128[] memory operatorAssignedDetails = new uint128[](numOperators + 1);
125:      for (uint128 operatorId = 1; operatorId <= numOperators; operatorId++) {

// @audit cache `_pubKeys.length`
189:    validatorDetails = new ValidatorDetails[](_pubKeys.length);
191:    for (uint256 i; i < _pubKeys.length; i++) {
227:    numPendingValidators -= _pubKeys.length;

// @audit cache `_validatorDetails.length`
243:    if (_validatorDetails.length == 0) {
257:        _validatorDetails.length >
263:    for (uint128 i; i < _validatorDetails.length; i++) {
282:    numPendingValidators += _validatorDetails.length;

// @audit cache `_pubKeys.length`
396:    for (uint128 i; i < _pubKeys.length; i++) {
412:     numPendingValidators -= _pubKeys.length;

// @audit cache `_pubKeys.length`
425:     for (uint256 i; i < _pubKeys.length; i++) {

// @audit cache `operatorIdToValidatorDetails[operatorId].length()`
628:     if (operatorIdToValidatorDetails[operatorId].length() == 0) {
634:      operatorIdToValidatorDetails[operatorId].length() - 1
```

File: `swEXIT.sol`
```solidity
// @audit cache `requestsToProcess + 1`
143:    for (uint256 i = 1; i < requestsToProcess + 1; ) {
```

File: `Whitelist.sol`
```solidity
// @audit cache `_addresses.length`
 84:    for (uint256 i; i < _addresses.length; ) {
102:    for (uint256 i; i < _addresses.length; ) {
```

**Swell:** Fixed in commits [3c67e88](https://github.com/SwellNetwork/v3-contracts-lst/commit/3c67e88dbea1bb4cdf0bfeda27b40e71e494ef2c), [3f85df3](https://github.com/SwellNetwork/v3-contracts-lst/commit/3f85df3ba0e91b26e4234b15ad94f492fa6d46ec).

**Cyfrin:**
Verified.

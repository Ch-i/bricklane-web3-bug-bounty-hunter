---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-parcel-payroll-3-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-Parcel%20Payroll.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-parcel-payroll
title: '[I-01] Redundant or unused interfaces, enums, variables, modifiers and comments
  throughout the codebase'
vuln_class: []
---

# [I-01] Redundant or unused interfaces, enums, variables, modifiers and comments throughout the codebase

_Section severity (from Solodit section header): Informational_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-Parcel Payroll.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-Parcel%20Payroll.md)_

---

The `GnosisSafe` interface in `index` is only used as a parameter type in the `executeAllowanceTransfer` method, but it is not really needed as you can use a type of `address` instead. This way you can remove the `GnosisSafe` interface because its only method `execTransactionFromModule` is not used anywhere in the codebase.

The `Allowance` struct in `AllowanceModule` is not used anywhere and can be removed.

The `getTokenAllowance` method from the `AllowanceModule` interface is not used anywhere and can be removed.

The `Operation` enum in `Storage` is not used anywhere and can be removed.

The `MASTER_OPERATOR` storage variable in `Storage` is only written to but never read from and it is `internal` so it doesn't have a getter. It can be removed.

The `SENTINEL_UINT` constant in `Storage` is not used anywhere and can be removed.

There is no need in `Validators::isApprover` to check that `_addressToCheck != address(0)` . This is because in `Organizer::onboard` there is a `require` statement that enforces an `approver` address to not be `address(0)` . This means `_isApprover` will return `false` anyway, so the check is redundant and can be removed.

There is no need for the `require(_addressToCheck != address(0), "CS003");` check in `isOrgOnboarded` in `Validators`, because `Organizer::onboard` uses only `msg.sender` as the key in the `orgs` mapping, so it can't be `address(0)`. The check can be removed as it is redundant and wastes gas.

There is actually no need to do the `isOrgOnboarded` check in `Validators::isApprover`, because even if it is omitted, the `_isApprover` method will return `false` if an Org was not onboarded. My recommendation here is to remove the `Validators` smart contract and just use

```solidity
require(_addressToCheck != SENTINEL_ADDRESS);
orgs[_safeAddress].approvers[_addressToCheck] != address(0);
```

to check if an address is an approver for a Gnosis Safe wallet.

The `onlyMultisig` modifier in `Modifiers` is redundant as it just enforces a function argument to have the value of `msg.sender`. Remove the modifier and the argument checked and just use `msg.sender` directly instead.

Remove commented out imports in `Organizer` as the code is not used. Old code will be kept in old git commits so if you need them again you can get them from there, but there is no need to keep code commented out like this.

The `EIP712Domain` struct definition in `Signature` is not needed as it is not really used as it is actually hardcoded as a string in the `EIP712_DOMAIN_TYPEHASH` hash calculation. The struct definition can be removed as it is redundant.

The `PayrollTx` struct definition in `Signature` is not needed as it only contains one field. Remove the struct and its usage in `validatePayrollTxHashes` and use the `rootHash` field directly instead . Move the `// hash = encodeTransactionData(recipient, tokenAddress, amount, nonce)` comment to the NatSpec `@param` definition of `rootHash` in `validatePayrollTxHashes`.

Remove the `signer` variable in `validatePayrollTxHashes` and just return its value - no need to extract a variable if it's only going to be used once.

Remove the `encodedHash` variable in `PayrollManager::encodeTransactionData` and just directly return its value since it is only used once.

Remove the `erc20` variables and use their values directly in `PayrollManager::executePayroll` as they are only used once in their scopes.

Remove the `allowance` and `to` variables and use their values directly in `PayrollManager::execTransactionFromGnosis` as they are only used once.

Remove the `signature` parameter from `PayrollManager::execTransactionFromGnosis` as its value is always `bytes("")` - just pass this value directly to the `executeAllowanceTransfer` call instead.

Remove the local array variable `validatedRoots` in `PayrollManager::executePayroll` as all of its values are `true` anyway so it is redundant.

The `flag` parameter of `packPayoutNonce` is always `true`, so it can be removed as well as the code that is executed when it is `false`, because it is never executed (dead code).

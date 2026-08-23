---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-11-cyfrin-securitize-matchhandler-v2-0-2-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-11T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-11-cyfrin-securitize-matchHandler-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-11-cyfrin-securitize-matchhandler-v2-0
title: '`MatchHandler::addOperator, removeOperator` call the public `grantRole, revokeRole`
  instead of the internal `_grantRole, _revokeRole`'
vuln_class: []
---

# `MatchHandler::addOperator, removeOperator` call the public `grantRole, revokeRole` instead of the internal `_grantRole, _revokeRole`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-11-cyfrin-securitize-matchHandler-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-11-cyfrin-securitize-matchHandler-v2.0.md)_

---

**Description:** `MatchHandler::addOperator` and `MatchHandler::removeOperator` are already gated by `onlyRole(DEFAULT_ADMIN_ROLE)`, yet they call OpenZeppelin's public `grantRole`, `revokeRole` (`contracts/ats/MatchHandler.sol:175` and `contracts/ats/MatchHandler.sol:180`). Those public functions carry their own `onlyRole(getRoleAdmin(OPERATOR_ROLE))` modifier; since `OPERATOR_ROLE` is administered by `DEFAULT_ADMIN_ROLE` (the OpenZeppelin default), that built-in check re-verifies the caller's `DEFAULT_ADMIN_ROLE` membership that the wrapper's own modifier already checked, costing a redundant warm `SLOAD` (and the surrounding `hasRole` plumbing) on every call. The contract's own `initialize` already uses the internal `_grantRole` (`contracts/ats/MatchHandler.sol:112-113`), so the two operator setters are inconsistent with it.

```solidity
contracts/ats/MatchHandler.sol
175:        grantRole(OPERATOR_ROLE, operator);
180:        revokeRole(OPERATOR_ROLE, operator);
```

**Recommended Mitigation:** Call the internal variants, which perform the role write without the redundant access check (the `onlyRole(DEFAULT_ADMIN_ROLE)` wrapper already authorizes the caller, matching what `initialize` does):

```solidity
_grantRole(OPERATOR_ROLE, operator);   // addOperator
_revokeRole(OPERATOR_ROLE, operator);  // removeOperator
```

This is an admin-only, infrequently-called path, so the per-call saving is small; the change also restores consistency with `initialize`.

**Securitize:** Fixed in commit [`a54fa5d`](https://github.com/securitize-io/bc-ats-sc/commit/a54fa5dd9600df5a0fab2ebc6f8be823a6fdb4c6)

**Cyfrin:** Verified.

\clearpage

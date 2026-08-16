---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-11-cyfrin-securitize-matchhandler-v2-0-1-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-06-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-11-cyfrin-securitize-matchHandler-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-11-cyfrin-securitize-matchhandler-v2-0
title: '`MatchHandler` has several minor code-quality and documentation mismatches'
vuln_class: []
---

# `MatchHandler` has several minor code-quality and documentation mismatches

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-11-cyfrin-securitize-matchHandler-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-11-cyfrin-securitize-matchHandler-v2.0.md)_

---

**Description:** A set of low-risk inconsistencies and omissions:

_1. Attribute arrays are forwarded without length validation_
`MatchHandler::_updateBuyerInRegistry` passes the buyer's three attribute arrays straight to `updateInvestor`, which requires them to be equal length; a malformed `Investor` reverts deep in the registry rather than at the contract boundary.

```solidity
// contracts/ats/MatchHandler.sol:247
registry.updateInvestor(buyer.blockchainId, "", buyer.country, wallets,
    buyer.investorAttributeIds, buyer.investorAttributeValues, buyer.investorAttributeExpirations); // @audit no local length check
// external/dstoken/contracts/registry/RegistryService.sol:69
require(_attributeValues.length == _attributeIds.length, "Wrong length of parameters");
```

**2. `Investor` NatSpec documents a field that is intentionally absent.**
The NatSpec for `IMatchHandler.Investor` documents a `collisionHash` parameter, but the struct has no such field (`contracts/interfaces/IMatchHandler.sol:36,43-50`). This is a documentation mismatch : `doc/architecture.md:86-90` explicitly states that callers do not need to provide the registry's `collisionHash` argument and that `_updateBuyerInRegistry` intentionally passes `""` (`MatchHandler.sol:249`). DS Protocol v4.1.0 only stores that value when registering a new investor and does not validate it or use it in an on-chain security check.

**3. Role naming drift.**
The dev brief and audit-scope PDF refer to the settlement role as `OWNER_ROLE`; the code defines and uses `OPERATOR_ROLE` (`MatchHandler.sol:79`).

**4. No `CustodialWalletSet` event on initialization.**
`initialize` sets `custodialWallet` without emitting `CustodialWalletSet` (`MatchHandler.sol:115`), while `setCustodialWallet` does (`:192`). Indexers tracking only that event miss the initial value.

**Recommended Mitigation:**
- Validate `investorAttributeIds.length == investorAttributeValues.length == investorAttributeExpirations.length` in `matchOrder` before the registry call.
- Remove the stale `@param collisionHash` entry from the `Investor` NatSpec, or clarify nearby documentation that the registry argument is intentionally supplied internally as `""`. Do not add an ABI field unless the intended integration changes and operators are expected to provide this value.
- Align documentation to use `OPERATOR_ROLE`.
- Emit `CustodialWalletSet(address(0), custodialWallet_)` in `initialize`.

**Securitize:**
1. Acknowledged.
2. Fixed in commit [`dc4ca3d`](https://github.com/securitize-io/bc-ats-sc/commit/dc4ca3d74cefe5771841abe4335b0fb10bbdb0ca)
3. Readme and project documentation and natSpec were updated
4. Acknowledged. Typically we never emit events during storage initialization, only for updates

**Cyfrin:** 2. Verified.

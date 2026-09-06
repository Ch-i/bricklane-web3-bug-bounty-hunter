---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-3-14
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`ArmadaGovernor::initialize` populates selector maps via keccak strings, drifting
  silently on cross-contract rename'
vuln_class: []
---

# `ArmadaGovernor::initialize` populates selector maps via keccak strings, drifting silently on cross-contract rename

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `ArmadaGovernor::initialize` (`contracts/governance/ArmadaGovernor.sol:344-411`) populates `extendedSelectors` and `standardSelectors` using two patterns:

1. `this.<func>.selector` for governor-local functions (lines 344-350) - compile-time safe; renaming the function breaks the build.
2. `bytes4(keccak256("<signature>"))` string literals for every selector that targets another in-scope contract (lines 352-411, e.g. `setShieldFee(uint120)`, `setBaseArmadaTake(uint256)`, `addStewardBudgetToken(address,uint256,uint256)`, `authorizeAdapter(address)`, etc.) - NOT compile-time checked

**Impact:** If a target function is renamed, has a parameter type changed (e.g. `uint120` -> `uint128`), or is removed, the keccak literal still compiles and the entry silently no longer matches any real function. The selector classification then defaults to the fail-closed Extended branch, which is safe for `standardSelectors` entries but materially weaker for `extendedSelectors` entries that are intended to FORCE Extended (the `multicall, execute, callContract` deny-list at lines 385-391, fee setters, adapter authorization, etc.) - those would silently classify as Extended only via the default, with no record that the explicit deny was lost.

**Recommended Mitigation:** Replace each keccak-string literal that targets a function in an in-scope contract with the interface-bound form `IInterface.funcName.selector`, which is computed at compile time and breaks the build on rename or signature change.

For UUPS upgrade selectors (lines 352-353), bind to the OZ UUPS interface (`IERC1967` / `UUPSUpgradeable`) the proxy actually inherits.

The wrapper deny-list at lines 385-391 (`callContract, functionCall, functionCallWithValue, functionDelegateCall, multicall, execute`) targets generic relay shapes across arbitrary contracts and has no single canonical interface; keccak strings are acceptable there. Add a NatSpec note distinguishing the two cases so future maintainers do not "fix" the wrapper list to interface form.

**Armada:** Acknowledged.

\clearpage

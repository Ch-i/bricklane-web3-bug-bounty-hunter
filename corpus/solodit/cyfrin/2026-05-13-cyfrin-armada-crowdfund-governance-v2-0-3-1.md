---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-3-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: Missing input validation in value-movers, `AdapterRegistry`, and `ArmadaRedemption::redeem`
vuln_class: []
---

# Missing input validation in value-movers, `AdapterRegistry`, and `ArmadaRedemption::redeem`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** Multiple externally-facing value-moving and admin functions lack basic input validation. Enumerated sub-items:

1. **`ArmadaTreasuryGov::distribute`** — `contracts/governance/ArmadaTreasuryGov.sol:139-144` — missing `amount > 0`. A zero-amount call inserts a zero record into the append-only outflow history and silently invokes the recipient's fallback. Unlike `stewardSpend`, which requires `amount > 0`, `distribute` has no such guard.
2. **`ArmadaTreasuryGov::transferTo`** — `contracts/governance/ArmadaTreasuryGov.sol:477-485` — missing `amount > 0`. A future wind-down replacement that passes zero invokes the recipient's fallback with no value change.
3. **`ArmadaTreasuryGov::transferETHTo`** — `contracts/governance/ArmadaTreasuryGov.sol:486-492` — missing `amount > 0`. `recipient.call{value: 0}("")` still invokes the recipient's fallback.
4. **`AdapterRegistry::deauthorizeAdapter, fullDeauthorizeAdapter`** — `contracts/governance/AdapterRegistry.sol:57-76` — missing `adapter != address(0)` guard. Current behaviour produces a status-error revert on the zero address, which is misleading. `authorizeAdapter` does check — the siblings are inconsistent.
5. **`ArmadaRedemption::redeem`** — `contracts/governance/ArmadaRedemption.sol:160` — missing explicit `tokens[i] != address(0)` check inside the loop. The zero address currently reverts via the ABI decoder after the ARM transfer, which rolls back correctly but is inconsistent with the explicit ARM-token zero check above it.
6. **`ArmadaGovernor::setExcludedAddresses`** — `contracts/governance/ArmadaGovernor.sol:424-436` — missing duplicate-address check. The loop rejects `address(0)` and `treasuryAddress` but accepts the same non-treasury address pushed twice. `_initProposal:855-859` then sums `balanceOf` across the list, so a duplicated entry double-counts that address's balance into `excludedBalance`, artificially lowering `snapshotEligibleSupply = totalSupply - excludedBalance` and the resulting quorum threshold. The `excludedAddressesLocked` flag makes this permanent without a UUPS upgrade. The spec at `specs/GOVERNANCE.md:86` defines the denominator as set subtraction (`totalSupply - treasury - excludedAddresses`), so duplicate counting violates spec intent.

**Spec-Intent Gap:**

Spec is silent on input validation for these paths. The concern is cross-function asymmetry — `stewardSpend` (`:152-154`) and `authorizeAdapter` (`AdapterRegistry.sol:44-53`) enforce input guards (`amount > 0`, `adapter != address(0)`); their siblings do not. Zero-amount outflow records and zero-address deauthorisations pollute append-only storage with entries that carry no economic meaning. For sub-item 6, the spec states the quorum-denominator formula in set form but the contract permits a multiset configuration.

**Impact:** Defense-in-depth gaps. Items (1)-(3) allow zero-amount recipient-fallback invocations that are harmless today but remove an obvious guard against future regressions. Item (4) produces misleading error messages. Item (5) wastes a revert path that could be caught earlier. Item (6) permanently inflates `excludedBalance` and lowers the quorum threshold below the spec-stated value if a duplicate is configured at bootstrap.

**Recommended Mitigation:** Per sub-item:

```solidity
// (1) ArmadaTreasuryGov::distribute
require(amount > 0, "ArmadaTreasuryGov: zero amount");

// (2) ArmadaTreasuryGov::transferTo
require(amount > 0, "ArmadaTreasuryGov: zero amount");

// (3) ArmadaTreasuryGov::transferETHTo
require(amount > 0, "ArmadaTreasuryGov: zero amount");

// (4) AdapterRegistry::deauthorizeAdapter, fullDeauthorizeAdapter
require(adapter != address(0), "AdapterRegistry: zero adapter");

// (5) ArmadaRedemption::redeem, inside the tokens[] loop
require(tokens[i] != address(0), "ArmadaRedemption: zero token");

// (6) ArmadaGovernor::setExcludedAddresses — require strictly-ascending order,
// which dedups in O(n) without a memory mapping
for (uint256 i; i < addrs.length; i++) {
    if (addrs[i] == address(0)) revert Gov_ZeroAddress();
    if (addrs[i] == treasuryAddress) revert Gov_TreasuryAlreadyExcluded();
    if (i != 0 && addrs[i] <= addrs[i - 1]) revert Gov_NotSortedAscending();
    _excludedFromQuorum.push(addrs[i]);
}
```

**Armada:** Fixed in commit [2762a72](https://github.com/ship-armada/armada-poc/commit/2762a72ec8d1a1ce0b876774b6076981939b960d).

**Cyfrin:** Verified.

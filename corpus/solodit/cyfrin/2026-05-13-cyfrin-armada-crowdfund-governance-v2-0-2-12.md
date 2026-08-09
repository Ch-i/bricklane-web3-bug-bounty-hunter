---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-2-12
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`ArmadaGovernor::addExtendedSelector, addStandardSelector` accept dual-map
  state; later removal silently downgrades'
vuln_class: []
---

# `ArmadaGovernor::addExtendedSelector, addStandardSelector` accept dual-map state; later removal silently downgrades

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `ArmadaGovernor` keeps two parallel selector classification maps - `extendedSelectors` and `standardSelectors` - that the spec at `specs/GOVERNANCE.md` treats as disjoint partitions. The classification setters do not enforce the disjointness:

- `addExtendedSelector` (`contracts/governance/ArmadaGovernor.sol:515-521`) only rejects double-add into `extendedSelectors`; it does not check `standardSelectors[selector]`.
- `addStandardSelector` (`contracts/governance/ArmadaGovernor.sol:536-540`) has no guards at all - it does not reject when the selector is already in `extendedSelectors`, nor when it is already in `standardSelectors`.

A selector can therefore be `true` in both maps simultaneously. At classification time `_classifyProposal:1134` checks `extendedSelectors` first and short-circuits, so Extended wins and the latent `standardSelectors` entry is shadowed at runtime. The shadowed entry survives indefinitely.

The hazard surfaces at the next state edit. If governance later calls `removeExtendedSelector(X)` expecting the selector to fall through to the `:1160` fail-closed default (which would keep it Extended), the latent `standardSelectors[X] = true` activates and the selector drops to Standard. The symmetric case (`removeStandardSelector(X)` while `extendedSelectors[X]` is true) is a no-op masquerading as a real change.

**Impact:** A governance reviewer comparing the proposed `removeExtendedSelector(X)` against the on-chain `extendedSelectors[X] = true` value sees a removal that, by their reading of the spec, leaves X in the unclassified-fail-closed state (still Extended at runtime). The latent `standardSelectors[X]` entry, which is not part of the proposal under review, silently flips X from Extended to Standard quorum on execution - bypassing the higher quorum and longer timelock the spec assigns to Extended actions for that selector. The reverse case hides the absence of an intended state change.

**Recommended Mitigation:** Enforce mutual exclusion in both setters. Either add explicit cross-map guards:

```solidity
error Gov_SelectorAlreadyStandard();

function addExtendedSelector(bytes4 selector) external {
    if (msg.sender != address(timelock)) revert Gov_NotTimelock();
    if (extendedSelectors[selector]) revert Gov_SelectorAlreadyExtended();
    if (standardSelectors[selector]) revert Gov_SelectorAlreadyStandard();
    extendedSelectors[selector] = true;
    emit ExtendedSelectorAdded(selector);
}

function addStandardSelector(bytes4 selector) external {
    if (msg.sender != address(timelock)) revert Gov_NotTimelock();
    if (standardSelectors[selector]) revert Gov_SelectorAlreadyStandard();
    if (extendedSelectors[selector]) revert Gov_SelectorAlreadyExtended();
    standardSelectors[selector] = true;
    emit StandardSelectorAdded(selector);
}
```

Also `ArmadaGovernor::removeStandardSelector` has no check to revert if the selector being removed is not a standard selector while `removeExtendedSelector` has this style of check.

Or collapse both maps into a single classification mapping where the type system forbids the contradictory state:

```solidity
enum Classification { Unclassified, Standard, Extended }
mapping(bytes4 selector => Classification classification) public selectorClassification;
```

**Armada:** Fixed in commits [77f75b8](https://github.com/ship-armada/armada-poc/commit/77f75b8e160da2cce2fc757bfc392bbcadbfcf38), [e02de88](https://github.com/ship-armada/armada-poc/commit/e02de88ea169fb135a22c7156483426d9102ba13).

**Cyfrin:** Verified.

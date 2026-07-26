---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-4-8
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: '`RootValidatorUpdated` event is misleading: the root validator is never updated'
vuln_class: []
---

# `RootValidatorUpdated` event is misleading: the root validator is never updated

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** `ValidationManager::_setRootValidator` emits `RootValidatorUpdated`, but the only caller is `OnChainLab::initialize` (line 168), which sets the immutable `DEFAULT_ROOT_VALIDATOR` once. There is no code path that ever changes the root validator after initialization. An off-chain consumer subscribing to `RootValidatorUpdated` for rotation tracking would mis-model the system as supporting rotation.

```solidity
src/core/ValidationManager.sol
89:    /// @notice Sets the root validator for the account
90:    /// @dev This function sets the root validator for the account and emits an event
91:    /// @param _rootValidator The new root ValidationId to set
92:    function _setRootValidator(ValidationId _rootValidator) internal {
93:        ValidationStorage storage vs = _validationStorage();
94:        vs.rootValidator = _rootValidator;
95:        emit IOnChainLab.RootValidatorUpdated(_rootValidator);
96:    }

src/OnChainLab.sol
168:        _setRootValidator(DEFAULT_ROOT_VALIDATOR);
```

**Recommended Mitigation:** Rename the event to `RootValidatorSet` (one-shot semantics) or, more simply, fold the assignment into `initialize` and drop `_setRootValidator` entirely.

**Molecule:** Fixed in commit [64dd291](https://github.com/moleculeprotocol/onchainlabs/commit/64dd291).

**Cyfrin:** Verified.

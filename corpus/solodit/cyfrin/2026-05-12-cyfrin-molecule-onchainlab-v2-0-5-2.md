---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-5-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: Unused locals and parameters in `ValidationManager::_validateUserOp`
vuln_class: []
---

# Unused locals and parameters in `ValidationManager::_validateUserOp`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** `ValidationManager::_validateUserOp` declares two unused locals (`vs`, `userOpSig`) and accepts an unused parameter (`vMode`). It also creates a memory copy of `op` that is never modified; since `IValidator::validateUserOp` accepts `calldata`, passing the memory copy forces an extra ABI re-encoding hop versus forwarding the calldata reference directly. The function is on the hot validation path (called for every UserOperation), so the wasted work is per-tx.

```solidity
src/core/ValidationManager.sol
144:    function _validateUserOp(
145:        ValidationMode vMode,
146:        ValidationId vId,
147:        PackedUserOperation calldata op,
148:        bytes32 userOpHash
149:    ) internal returns (ValidationData validationData) {
150:        // Get the ValidationStorage object from the account's storage
151:        ValidationStorage storage vs = _validationStorage();
152:        // Save the userOp to the memory so we can modify it
153:        PackedUserOperation memory userOp = op;
154:        // Extract the signature from the userOp
155:        bytes calldata userOpSig = op.signature;
156:        unchecked {
...
165:            validationData = ValidationData.wrap(ValidatorLib.getValidator(vId).validateUserOp(userOp, userOpHash));
166:        }
167:    }
```

`vMode` is also passed unconditionally from `OnChainLab::validateUserOp` (line 351) where it is hard-coded to `0x01`.

**Recommended Mitigation:** Drop `vMode`, `vs`, `userOpSig`, and the memory copy. Forward the calldata `op` directly:

```solidity
function _validateUserOp(
    ValidationId vId,
    PackedUserOperation calldata op,
    bytes32 userOpHash
) internal returns (ValidationData validationData) {
    unchecked {
        ValidationType vType = ValidatorLib.getType(vId);
        if (vType != VALIDATION_TYPE_ROOT) revert InvalidValidationType();
        validationData = ValidationData.wrap(
            ValidatorLib.getValidator(vId).validateUserOp(op, userOpHash)
        );
    }
}
```

Update the single caller `OnChainLab::validateUserOp` to drop the `vMode` argument.

**Molecule:** Fixed in commit [f282373](https://github.com/moleculeprotocol/onchainlabs/commit/f282373).

**Cyfrin:** Verified.

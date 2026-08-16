---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-4-6
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: Use named mapping parameters
vuln_class: []
---

# Use named mapping parameters

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** Several state-variable mappings in scope use unnamed key/value types. Named mappings (`mapping(KeyType keyName => ValueType valueName)`) are documentation that survives in IDEs and on Etherscan and reduce the chance that a future caller mis-passes arguments at the call site. Several other mappings in scope are already correctly named (`mapping(bytes32 requestId => bool used) public usedRequestId;`) - the listed ones are inconsistent with the surrounding style.

```solidity
src/core/ExecutorManager.sol
18:        mapping(IExecutor => ExecutorConfig) executorConfig;

src/core/SelectorManager.sol
20:        mapping(bytes4 => SelectorConfig) selectorConfig;

src/core/ValidationManager.sol
50:        mapping(ValidationId => ValidationConfig) validationConfig;

src/modules/validator/RootValidator.sol
32:    mapping(address => EcdsaValidatorStorage) public ecdsaValidatorStorage;

src/identity/MoleculeOclDidRegistry.sol
69:    mapping(bytes32 provider => mapping(bytes32 subject => IDidVerifier)) public verifier;
```

The `verifier` mapping at line 69 is named on the outer keys but the inner value (`IDidVerifier`) is unnamed - supply a value name for symmetry.

**Recommended Mitigation:**
```solidity
mapping(IExecutor executor => ExecutorConfig config) executorConfig;
mapping(bytes4 selector => SelectorConfig config) selectorConfig;
mapping(ValidationId vId => ValidationConfig config) validationConfig;
mapping(address smartAccount => EcdsaValidatorStorage store) public ecdsaValidatorStorage;
mapping(bytes32 provider => mapping(bytes32 subject => IDidVerifier verifier)) public verifier;
```

**Molecule:** Fixed in commit [4c7d579](https://github.com/moleculeprotocol/onchainlabs/commit/4c7d579).

**Cyfrin:** Verified.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-3-10
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: '`OnChainLab::isModuleInstalled` is not checking RootValidator'
vuln_class: []
---

# `OnChainLab::isModuleInstalled` is not checking RootValidator

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** `isModuleInstalled` function in `OnChainLab` checking weather the module is installed or not, it only accepts two types of moduleTypes (Executor and Fallback).

> src/OnChainLab.sol#isModuleInstalled
```solidity
    function isModuleInstalled(uint256 moduleTypeId, address module, bytes calldata additionalContext) ... {
        if (moduleTypeId == MODULE_TYPE_EXECUTOR) {
            return _executorConfig(IExecutor(module)).installed;
        } else if (moduleTypeId == MODULE_TYPE_FALLBACK) {
            if (additionalContext.length < 4) {
                return false;
            }
            return _selectorConfig(bytes4(additionalContext[0:4])).module == module;
        } else {
            return false;
        }
    }
```

Passing `MODULE_TYPE_VALIDATOR` by providing `rootValidator` module will result in `false` although it is true and installed in the wallet setup.

This will affect 3rd party contracts integrating with the wallet that check whether the module is installed before triggering.


**Recommended Mitigation:** We should return true if the module passed is rootValidator and type is `MODULE_TYPE_VALIDATOR` so that the function shows that it has RootValidator as a valid Validator Module.

**Molecule:** Fixed in [59b0a4d](https://github.com/moleculeprotocol/onchainlabs/commit/59b0a4d).

**Cyfrin:** Verified.

\clearpage

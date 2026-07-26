---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-2-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: '`OnchainLab::uninstallModule` allows uninstalling Executors that are not installed,
  breaking EIP-7579'
vuln_class: []
---

# `OnchainLab::uninstallModule` allows uninstalling Executors that are not installed, breaking EIP-7579

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** In `uninstallModule`, the `MODULE_TYPE_EXECUTOR` branch calls `_clearExecutorData(IExecutor(module))` and then, when `shouldCallOnUninstall` is true, `ModuleLib.uninstallModule(module, deInitData)` without first checking that the executor is actually installed.

`ExecutorManager._clearExecutorData` only sets `config.installed = false` and does not revert if the executor was never installed. By contrast, the `MODULE_TYPE_FALLBACK` path validates state before clearing: it derives the module from storage via `_clearSelectorData(selector)` and reverts with `InvalidSelector` if the selector is not bound to the given `module` (and if `target == address(0)`).

As a result, a call routed through the EntryPoint can “uninstall” an executor address that was never installed: storage may already be `installed == false`, yet the account can still execute an external `onUninstall` on that address and emit `ModuleUninstalled`. That does not match the usual ERC-7579 expectation that uninstalling a module that is not installed should fail (revert), and it can desynchronize on-chain state, events, and off-chain indexers from the true installation set.

This violates EIP7579 standards where the wallet should not be able to uninstall a module that is not installed

https://eips.ethereum.org/EIPS/eip-7579#account
```solidity
    /**
     * @dev Uninstalls a Module of a certain type on the smart account
     * @param moduleTypeId the module type ID according the ERC-7579 spec
     * @param module the module address
     * @param deInitData arbitrary data that may be required on the module during `onInstall`
     * initialization.
     *
     * MUST implement authorization control
     * MUST call `onUninstall` on the module with the `deInitData` parameter if provided
     * MUST emit ModuleUninstalled event
>>   * MUST revert if the module is not installed or the deInitialization on the module failed
     */
    function uninstallModule(uint256 moduleTypeId, address module, bytes calldata deInitData) external;

```

**Impact:**
- Allowing the wallet ro uninstall a module that is not yet installed, this can lead to unexpected behaviour in some scenarious is the module itself is not checking installation.
- Violating EIP7579 which OnChainLab wallet is compatible with.

**Recommended Mitigation:** We should revert when calling uninstall module if the module is not installed aas Executor, same as implemented in fallback

```diff
    function uninstallModule(uint256 moduleType, address module, bytes calldata deInitData) ... {
        bool shouldCallOnUninstall = true;
        if (moduleType == MODULE_TYPE_EXECUTOR) {
+           if (!_executorConfig(IExecutor(module)).installed) {
+               revert InvalidExecutor();
+           }
            _clearExecutorData(IExecutor(module));
        } else if (moduleType == MODULE_TYPE_FALLBACK) {
            ...
        } else {
            revert InvalidModuleType();
        }
        ...
    }

```


**Molecule:** Fixed in [3937d6f](https://github.com/moleculeprotocol/onchainlabs/commit/3937d6f).

**Cyfrin:** Verified.

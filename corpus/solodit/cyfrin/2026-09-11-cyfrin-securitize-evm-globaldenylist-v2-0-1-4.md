---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-11-cyfrin-securitize-evm-globaldenylist-v2-0-1-4
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-09-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-11-cyfrin-securitize-evm-globaldenylist-v2-0
title: '`ServiceConsumer::setDSService` accepts an address with no code, halting all
  transfers and issuance on the wired token'
vuln_class: []
---

# `ServiceConsumer::setDSService` accepts an address with no code, halting all transfers and issuance on the wired token

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md)_

---

**Description:** `ServiceConsumer::setDSService` writes the supplied address into the service registry with no validation at all: no zero check, no service-id whitelist, and no code-size check.

`ComplianceServicePermissionless::_isGloballyDenylisted` guards only the `address(0)` case and calls through for every other value. That call returns `bool`, so Solidity 0.8 emits an `extcodesize` check on the target before decoding the return data. A wired address holding no code fails that check and the call reverts with empty revert data.

The deployment task does not compensate. `deploy-all` resolves the supplied address with `ethers.getContractAt`, which validates address format and EIP-55 checksum client-side but never queries the chain for code, so an all-lowercase typo or a pasted EOA passes straight through to `set-services`.

**Impact:** Wiring a codeless address into the `GLOBAL_DENYLIST_MANAGER` slot halts the token. `transfer`, `transferFrom`, every `issueTokens` variant, `preTransferCheck` and `getComplianceTransferableTokens` all revert. Transfers and issuance stop rather than degrade.

**Recommended Mitigation:** * Validate in the registry:

```diff
function setDSService(uint256 _serviceId, address _address) public override onlyMaster returns (bool) {
+   if (_address != address(0) && _address.code.length == 0) revert ServiceAddressHasNoCode();
    services[_serviceId] = _address;
    emit DSServiceSet(_serviceId, _address);
    return true;
}
```

* Validate in the deployment task:

```typescript
if ((await hre.ethers.provider.getCode(args.globalDenylistManagerAddress)) === '0x') {
  throw new Error(`No contract at ${args.globalDenylistManagerAddress}`);
}
// catch interface drift
await globalDenylistManager.isGloballyDenylisted(hre.ethers.ZeroAddress);
```

**Securitize:** Fixed in commit [cbfcd9e](https://github.com/securitize-io/dstoken/commit/cbfcd9e332f8f81522c0cd709be16b3eef8e496e).

**Cyfrin:** Verified; the script guard was added but `ServiceConsumer::setDSService` remains unchanged so technically still possible in other cases.

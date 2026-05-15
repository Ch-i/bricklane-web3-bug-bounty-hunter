---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-2-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Asymmetry enforcement between `TokenIssuer::registerInvestor`, `WalletRegistrar::registerWallet`
  and `SecuritizeSwap::_registerNewInvestor`
vuln_class: []
---

# Asymmetry enforcement between `TokenIssuer::registerInvestor`, `WalletRegistrar::registerWallet` and `SecuritizeSwap::_registerNewInvestor`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** In `TokenIssuer::registerInvestor`, if the user isn't already an investor they get registered and must have 3 specific attributes set:
```solidity
if (!getRegistryService().isInvestor(_id)) {
    getRegistryService().registerInvestor(_id, _collisionHash);
    getRegistryService().setCountry(_id, _country);

    if (_attributeValues.length > 0) {
        require(_attributeValues.length == 3, "Wrong length of parameters");
        getRegistryService().setAttribute(_id, KYC_APPROVED, _attributeValues[0], _attributeExpirations[0], "");
        getRegistryService().setAttribute(_id, ACCREDITED, _attributeValues[1], _attributeExpirations[1], "");
        getRegistryService().setAttribute(_id, QUALIFIED, _attributeValues[2], _attributeExpirations[2], "");
    }
```

But in `WalletRegistrar::registerWallet` and `SecuritizeSwap::_registerNewInvestor` if the user isn't already an investor, they get registered but the same attribute logic is not there. Instead it is more generic appearing to over-write anything that exists and not enforcing existence of KYC_APPROVED, ACCREDITED or QUALIFIED attributes:
```solidity
if (!registryService.isInvestor(_id)) {
    registryService.registerInvestor(_id, _collisionHash);
    registryService.setCountry(_id, _country);
}

for (uint256 i = 0; i < _wallets.length; i++) {
    if (registryService.isWallet(_wallets[i])) {
        require(CommonUtils.isEqualString(registryService.getInvestor(_wallets[i]), _id), "Wallet belongs to a different investor");
    } else {
        registryService.addWallet(_wallets[i], _id);
    }
}

for (uint256 i = 0; i < _attributeIds.length; i++) {
    registryService.setAttribute(_id, _attributeIds[i], _attributeValues[i], _attributeExpirations[i], "");
}
```

**Impact:** Going through `WalletRegistrar::registerWallet` or `SecuritizeSwap::_registerNewInvestor` an investor can be registered without the required attributes.

**Recommended Mitigation:** Harmonize the investor registration process to remove duplicated code and enforce the same requirements.

**Securitize:** Fixed in commit [72e54d2](https://github.com/securitize-io/dstoken/commit/72e54d2863f87cba2eda1535a4fc3f8902839ddc).

**Cyfrin:** Verified.

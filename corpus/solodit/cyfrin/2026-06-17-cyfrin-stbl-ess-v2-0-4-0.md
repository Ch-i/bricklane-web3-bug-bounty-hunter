---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-4-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: Stale OZ 4.x `__UUPSUpgradeable_init` calls in concrete UUPS implementations
  prevent compilation under OZ 5.x
vuln_class: []
---

# Stale OZ 4.x `__UUPSUpgradeable_init` calls in concrete UUPS implementations prevent compilation under OZ 5.x

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** All six concrete UUPS implementation contracts - `STBL_XLayer_Wrapper`, `STBL_XLayer_NFT_Vault`, `STBL_XLLayer_Token`, `STBL_XLayer_Asset_Issuer`, `STBL_XLayer_Asset_Vault`, and `STBL_XLayer_Asset_YieldDistributor` - in `stbl-contracts-evm-ess-common` call `__UUPSUpgradeable_init` inside their `initialize` functions, following the OpenZeppelin 4.x convention. In OZ 4.x this function existed as an empty no-op stub to fill the initializer chain. In OZ 5.0 it was removed entirely: `UUPSUpgradeable` carries no initializable storage, so the `__init` and `__init_unchained` stubs were dropped.

Calling an undefined function in Solidity is a compile-time error, so all six contracts cannot be compiled once OZ 5.x is resolved.

`package.json` declares `"@openzeppelin/contracts": "^5.4.0"` and `"@openzeppelin/contracts-upgradeable": "^5.4.0"`. The caret range permits any non-breaking 5.x release, and `npm` resolved both to `5.6.1` — the version in which `__UUPSUpgradeable_init` was removed. Had the version been pinned to exactly `5.4.0`, the function would still be present and compilation would succeed. The caret range is therefore a latent upgrade hazard: any `npm install` on a clean environment silently installs a version that breaks the build.

All six contracts - `STBL_XLayer_Wrapper`, `STBL_XLayer_NFT_Vault`, `STBL_XLLayer_Token`, `STBL_XLayer_Asset_Issuer`, `STBL_XLayer_Asset_Vault`, and `STBL_XLayer_Asset_YieldDistributor` - are affected. The same call also appears in `STBL_USST.sol` from the `@stbl-protocol/stbl-contracts-evm-core` external dependency, meaning the build failure extends beyond the in-scope contracts.

There is no runtime or funds-at-risk component. The failure is pre-deployment and has no exploitable security surface. It is documented here because the root cause (an OZ 4.x migration residue combined with an unpinned version range) is non-obvious: the build silently breaks on the next clean install without any change to the contract source.

**Recommended Mitigation:** Remove `__UUPSUpgradeable_init` from the `initialize` function of every affected concrete implementation. In OZ 5.x, UUPS contracts require no separate UUPS initializer call; the `_authorizeUpgrade` override and the `UUPSUpgradeable` inheritance are sufficient.

Additionally, pin the OZ dependency to the exact version in use (e.g. `"@openzeppelin/contracts": "5.6.1"`) to prevent a future `npm install` from silently resolving to a different version. Any future concrete implementation extending the abstract base contracts must not include `__UUPSUpgradeable_init`.

**STBL:** Fixed in commit [64d4887](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-ess-common/commit/64d4887b2c4b68c2964d4a4141c23982c75bbdd1).

**Cyfrin:** Verified. OZ dependency version has been set to `5.4.0`.

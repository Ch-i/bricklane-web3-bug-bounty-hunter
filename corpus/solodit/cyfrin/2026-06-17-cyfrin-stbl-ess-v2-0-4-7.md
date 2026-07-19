---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-4-7
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: '`STBL_ESS_Wrapper1` grants every asset vault `setApprovalForAll` on YLD that
  the asset vault never uses'
vuln_class: []
---

# `STBL_ESS_Wrapper1` grants every asset vault `setApprovalForAll` on YLD that the asset vault never uses

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `STBL_ESS_Wrapper1::__STBL_ESS_Wrapper1_init_unchained` grants `setApprovalForAll` on YLD to every configured asset vault in addition to the NFT vault:

```solidity
STBL_YLD.setApprovalForAll(address(STBL_ESS_NFT_Vault), true);
for (uint256 i = 0; i < _ratios.length; i++) {
    ...
    STBL_YLD.setApprovalForAll(address(AssetData.vault), true);
    ...
}
```

The NFT-vault grant is required because the NFT vault pulls YLD NFTs from the wrapper. The asset-vault grant has no caller: `STBL_T1e_Vault` (the base of `STBL_XLayer_Asset_Vault`) handles only ERC20 asset tokens and has no `IERC721`, no `STBL_YLD`, no `transferFrom` against the wrapper.

The wrapper holds YLD NFTs transiently in two windows during normal operation:

1. During `asset_issue`, iteration `i` calls `vault.depositERC20` before `Core.put` mints the NFT, so the wrapper still owns the NFTs minted by iterations `0..i-1` while `vault.depositERC20` is executing.
2. During `asset_Withdraw`, the wrapper first pulls every YLD NFT in the lot from the NFT vault, then iterates calling `issuer.withdraw` (which calls `vault.withdrawERC20`). While iteration `i`'s `vault.withdrawERC20` is executing, the wrapper still owns iterations `i+1..N`.

In both windows any contract approved-for-all on YLD by the wrapper can call `STBL_YLD.transferFrom(wrapper, _, _)` on those NFTs. The asset-vault grant turns every asset vault into such a contract.

**Impact:** Security Hardening

**Recommended Mitigation:** Drop the asset-vault grant from `__STBL_ESS_Wrapper1_init_unchained`. The NFT-vault grant is the only YLD approval the wrapper needs.

**STBL:** Fixed in commit [3bc5216](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-ess-common/commit/3bc5216a5138a64527c91400bd60c322c79e9fa1).

**Cyfrin:** Verified. The unused `setApprovalForAll` grant to asset vaults is removed from `__STBL_ESS_Wrapper1_init_unchained`, leaving only the required NFT-vault grant.

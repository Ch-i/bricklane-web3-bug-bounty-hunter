---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-3-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: upgradeable base contracts lack a storage gap
vuln_class: []
---

# upgradeable base contracts lack a storage gap

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** The abstract upgradeable base contracts `STBL_ESS_Wrapper1` and `STBL_ESS_NFT_Vault1` declare their state as a plain sequential list, with no trailing storage gap and no ERC-7201 namespaced storage. The concrete UUPS contracts `STBL_XLayer_Wrapper` and `STBL_XLayer_NFT_Vault` append their own state (`wrapper`, `assetTokens`, `_version`) immediately after the base slots.

Because the bases reserve no gap, inserting even one new variable into either base in a future implementation shifts every derived-contract slot down by one. After such an upgrade the derived contracts read mislabeled storage: `_version` and `assetTokens` resolve to slots holding stale base data, and `wrapper` (the address `onlyWrapper` trusts) resolves to unrelated data, breaking access control. The in-code comments at `STBL_ESS_NFT_Vault1.sol:62-69` ("Added after _version for upgrade compatibility") show the team already performs exactly this class of layout-affecting edit.

**Impact:** No effect on the current bytecode. The defect is latent: a future upgrade that appends a field to either base corrupts all derived storage. Rated Low as a defense-in-depth recommendation, since it reflects no current runtime bug.

**Recommended Mitigation:** Add a trailing `uint256[50] private __gap;` to `STBL_ESS_Wrapper1` and `STBL_ESS_NFT_Vault1` (decrementing it when fields are added), or migrate the bases to ERC-7201 namespaced storage.

**STBL:** Fixed in commit [f05b29d](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-ess-common/commit/f05b29d8a884a307c7700a4f0e3cc1c0b10e1fff).

**Cyfrin:** Verified. Added storage gap to base contracts. The concrete contracts that inherit from these base contracts **must** be freshly deployed, as this change modifies the storage layout of the previous version.

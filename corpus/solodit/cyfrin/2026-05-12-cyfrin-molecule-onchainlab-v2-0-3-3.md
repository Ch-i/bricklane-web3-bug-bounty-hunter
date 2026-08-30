---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-3-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: Upgrade-time storage and EIP-712 layout hazards in `OnChainLab, LabNFT, MoleculeOclDidRegistry`
vuln_class: []
---

# Upgrade-time storage and EIP-712 layout hazards in `OnChainLab, LabNFT, MoleculeOclDidRegistry`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** Sub-items:

- `OnChainLab` impl missing the standard storage-gap reservation pattern
- UUPS contracts (`MoleculeOclDidRegistry`, `LabNFT`) inherit OZ NON-upgradeable bases with no storage-gap reservation
- EIP712 ShortString fallback writes to impl storage if name/version >31 bytes (proxy then reads empty fallback)
- UUPS upgrade can swap EIP-712 `name`/`version` constants without on-chain assertion

**Files:**

`src/OnChainLab.sol:64-101`, `src/identity/MoleculeOclDidRegistry.sol:45-71, 111, 349`, `src/NFT/LabNFT.sol:17-46`.

**Recommended Mitigation:** Append a `uint256[50] private` storage-gap reservation to each affected contract; document a 31-byte limit on EIP-712 name/version OR migrate UUPS contracts to the OpenZeppelin upgradeable EIP712 base with its initializer; add an `_authorizeUpgrade` assertion that the new implementation's `eip712Domain` matches expected name/version.

**Molecule:** Fixed in [cf278bf](https://github.com/moleculeprotocol/onchainlabs/commit/cf278bf).

**Cyfrin:** Verified.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-4-7
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: '`LabNFT::setMintFee` lacks an upper bound'
vuln_class: []
---

# `LabNFT::setMintFee` lacks an upper bound

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** `LabNFT::setMintFee` accepts an arbitrary `uint256` fee with no upper bound. The contract documentation says the fee "approximates $5" (Constants.sol:98), but `setMintFee(type(uint256).max)` would silently brick `mint` (no payer can satisfy `msg.value >= fee`). The constructor seeds `mintFeeWei` with a sensible constant `INITIAL_LAB_MINT_FEE_WEI`, but the setter has no `MAX_MINT_FEE_WEI` cap. This is "Constructor vs setter validation inconsistency" applied to a magnitude bound: the deployment seeds a known-safe value, the setter permits any value.

```solidity
src/NFT/LabNFT.sol
69:        mintFeeWei = INITIAL_LAB_MINT_FEE_WEI;
70:        emit MintFeeUpdated(INITIAL_LAB_MINT_FEE_WEI);
...
94:    function setMintFee(uint256 newFee) external onlyRole(DEFAULT_ADMIN_ROLE) {
95:        mintFeeWei = newFee;
96:        emit MintFeeUpdated(newFee);
97:    }
```

**Recommended Mitigation:** Define `MAX_MINT_FEE_WEI` in `Constants.sol` (e.g., `1 ether`) and check it in the setter:

```solidity
function setMintFee(uint256 newFee) external onlyRole(DEFAULT_ADMIN_ROLE) {
    if (newFee > MAX_MINT_FEE_WEI) revert MintFeeTooHigh(newFee);
    mintFeeWei = newFee;
    emit MintFeeUpdated(newFee);
}
```

**Molecule:** Fixed in commit [c78277e](https://github.com/moleculeprotocol/onchainlabs/pull/4/changes/c78277edb222d8f31d8dd72992eec878728b5482).

**Cyfrin:** Verified.

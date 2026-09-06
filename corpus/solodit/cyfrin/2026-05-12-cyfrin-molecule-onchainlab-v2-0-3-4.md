---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-3-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: Missing input validation in admin setters across `OdfCoAttestVerifier, MoleculeOclDidRegistry,
  LabNFT`
vuln_class: []
---

# Missing input validation in admin setters across `OdfCoAttestVerifier, MoleculeOclDidRegistry, LabNFT`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** Five admin-setter input-validation gaps across three contracts. Each is independently low-severity (admin can fix with a re-call), but each is a footgun that contradicts a sister setter's stricter handling and should be made symmetric.

Sub-items:

- `OdfCoAttestVerifier` constructor accepts `_admin == address(0)`. Sister initializers in `LabNFT` and `MoleculeOclDidRegistry` enforce a zero-address check; the verifier does not. Permanently locks attester rotation if deployed with zero admin.

- `MoleculeOclDidRegistry::setVerifier` accepts `provider == bytes32(0)` and `subject == bytes32(0)`. Only the `_verifier` argument is validated. Allows admin to write a verifier under a nonsensical zero key, breaking the "no verifier configured" invariant.

- `LabNFT::setDerivationConfig` does not enforce `code.length > 0` on the supplied address. The directly-comparable `MoleculeOclDidRegistry::setDerivationConfig` does enforce it. Combined with the contract's set-once guard, a mistake locks LabNFT to a non-contract address until UUPS upgrade.

- `OdfCoAttestVerifier` per-attester setters cannot atomically swap both Kamu and Molecule attesters. Admin must use a temporary third address, and during the intermediate window (no pause exists on the verifier itself; only the DID registry has a pause) requests are accepted under the temporary attestation pair.

- `LabNFT::setMintFee` accepts `uint256.max` with no upper bound. The contract documentation says the fee approximates $5 (`Constants.sol:98`), but `setMintFee(type(uint256).max)` is not rejected; a typo or buggy admin call permanently bricks `mint` until corrected.

**Files:**

`src/identity/OdfCoAttestVerifier.sol:50-62, 70-90`, `src/identity/MoleculeOclDidRegistry.sol:154-161`, `src/NFT/LabNFT.sol:62-75, 102-107`.

**Recommended Mitigation:** Add:
* `require(_admin != address(0))` to `OdfCoAttestVerifier` constructor
* `require(provider != bytes32(0) && subject != bytes32(0))` to `MoleculeOclDidRegistry::setVerifier`
* `require(_config.code.length > 0)` to `LabNFT::setDerivationConfig` to mirror the registry sister setter
* an atomic `setAttesters(address kamu, address molecule)` to `OdfCoAttestVerifier` that swaps both in one call and enforces `kamu != molecule`
* a hard upper bound (e.g. `1 ether`) to `LabNFT::setMintFee`

**Molecule:** Fixed in commit [e85362b](https://github.com/moleculeprotocol/onchainlabs/commit/e85362b).

**Cyfrin:** Verified.

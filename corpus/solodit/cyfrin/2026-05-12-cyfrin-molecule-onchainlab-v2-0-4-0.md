---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-4-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: '`MintAndCreateAccount` deploy script omits `msg.value`; every invocation reverts
  post-deploy'
vuln_class: []
---

# `MintAndCreateAccount` deploy script omits `msg.value`; every invocation reverts post-deploy

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** `LabNFT.mint{value: msg.value}(to)` reverts when `msg.value < mintFeeWei` and the script broadcasts a 0-value tx.

**Files:**

`script/Lab/MintAndCreateAccount_v0.0.1.s.sol:31-33`.

**Recommended Mitigation:** `uint256 fee = LabNFT(labNft).mintFeeWei(); ... mintAndCreateAccount{value: fee}(user);`.

**Molecule:** Fixed in commit [5dd383c](https://github.com/moleculeprotocol/onchainlabs/commit/5dd383cdd2db27db18965d8021ab74a38911de29).

**Cyfrin:** Verified.

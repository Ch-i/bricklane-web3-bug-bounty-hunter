---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-28-tokentable-merkle-distributor-2-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-04-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-28-TokenTable-Merkle-Distributor.md
tags:
- firm:codespect
- report:2025-04-28-tokentable-merkle-distributor
title: '[I-01] The NFT Fee Handling is Incompatible with BIPS Type of Fees'
vuln_class: []
---

# [I-01] The NFT Fee Handling is Incompatible with BIPS Type of Fees

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-28-TokenTable-Merkle-Distributor.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-28-TokenTable-Merkle-Distributor.md)_

---

**Files:** [SimpleERC721MerkleDistributor.sol](https://github.com/EthSign/merkle-token-distributor/tree/96fedd0d945693149e0903c84502004bf819996c/src/core/extensions/SimpleERC721MerkleDistributor.sol#L16)

**Description:**

In case of ERC721 token distribution, the `claimedAmount` of the individual claim is representing the amount of tokens to be minted or transferred. As is the case with NFTs that variable can be small, i.e. 1 or 2. The `claimedAmount` is then passed into the `ITTUFeeCollector::getFee()` to calculate the exact fee amount charged to the claimer. While it works fine in case fixed fees are configured, it may not work as expected in case the protocol owner would like to charge fees based on bips, as the following calculation from the `ITTUFeeCollector::getFee()` may return zero in case of a low value of `claimedAmount`:

```solidity
tokensCollected = (tokenTransferred * feeBips) / BIPS_PRECISION;
```

The exact number when zero is returned depends on the value of `feeBips`.

**Impact:** Project needs to stick to fixed fees in case of ERC721 distributions, hence, fee policy flexibility is lost.

**Recommendation(s):** multiply the `claimedAmount` by `BIPS_PRECISION` before sending it to `ITTUFeeCollector::getFee()`.

**Status:** Acknowledged

**Update from TokenTable:** Acknowledged.

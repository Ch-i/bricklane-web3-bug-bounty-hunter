---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-28-tokentable-merkle-distributor-1-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-04-28T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-28-TokenTable-Merkle-Distributor.md
tags:
- firm:codespect
- report:2025-04-28-tokentable-merkle-distributor
title: '[L-01] Upgrade Permission for the Protocol Assigned to the Project Owner'
vuln_class: []
---

# [L-01] Upgrade Permission for the Protocol Assigned to the Project Owner

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-28-TokenTable-Merkle-Distributor.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-28-TokenTable-Merkle-Distributor.md)_

---

**Files:** [BaseMerkleDistributor.sol](https://github.com/EthSign/merkle-token-distributor/tree/96fedd0d945693149e0903c84502004bf819996c/src/core/BaseMerkleDistributor.sol#L293)

**Description:**

In the protocol, there are two roles:

- The `MDCreate2` contract controlled by TokenTable, which is responsible for initialising the contracts inheriting from `BaseMerkleDistributor` and includes the fee parameters required for token distribution;
- The contract owner, which is controlled by the project team responsible for the token distribution;

However, the upgrade privilege is assigned to the contract owner, which can lead to potential issues.

```solidity
// solhint-disable-next-line no-empty-blocks
function _authorizeUpgrade(address newImplementation) internal virtual override onlyOwner { }
```

It gives the project owner control to upgrade the distribution contracts.

**Impact:** The project team can upgrade the contract and set the deployer address to a malicious implementation they control. This allows them to bypass paying fees to TokenTable or even take the fees for themselves.

**Recommendation(s):** Removal of the upgradability option.

**Status:** Fixed

**Update from TokenTable:** Fixed in `c991b09f8da9eba24b0a789e6c7cb332d0394f40`.

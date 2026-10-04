---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-23-tokentable-ecdsa-distributor-0-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-04-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-23-TokenTable-ECDSA-Distributor.md
tags:
- firm:codespect
- report:2025-04-23-tokentable-ecdsa-distributor
title: '[M-01] The upgrade permission for the protocol was assigned to the wrong role.'
vuln_class: []
---

# [M-01] The upgrade permission for the protocol was assigned to the wrong role.

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-23-TokenTable-ECDSA-Distributor.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-23-TokenTable-ECDSA-Distributor.md)_

---

**Files:** [BaseECDSADistributor.sol](https://github.com/EthSign/ecdsa-token-distributor/tree/6d5db7f144d7468644313c98f9f310dbaadd1b01/src/core/BaseECDSADistributor.sol#L194)

**Description:**

In the protocol, there are two roles: one is the deployer contract controlled by the TokenTable, which is responsible for initializing the ECDSADistributor contract and includes the fee parameters required for token distribution. The second role is the contract owner, which is controlled by the project team responsible for the token distribution. However, the upgrade privilege is assigned to the contract owner, which can lead to potential issues.

```solidity
// solhint-disable-next-line no-empty-blocks
function _authorizeUpgrade(address newImplementation) internal virtual override onlyOwner { }
```

**Impact:** The project team can upgrade the ECDSADistributor contract and set the deployer address to a malicious implementation they control. This allows them to bypass paying fees to the TokenTable or even steal the fees.

**Recommendation:** It is recommended to transfer the upgrade authority to the deployer contract controlled by the TokenTable.

**Status:** Fixed

**Client response:** Fixed at [9c2cc47a5ed2dd745a3396f9c51733f9f25a69b6](https://github.com/EthSign/ecdsa-token-distributor/pull/8/commits/9c2cc47a5ed2dd745a3396f9c51733f9f25a69b6)

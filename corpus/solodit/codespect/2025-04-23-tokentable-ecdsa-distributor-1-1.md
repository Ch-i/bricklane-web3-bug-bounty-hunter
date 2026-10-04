---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-23-tokentable-ecdsa-distributor-1-1
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-04-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-23-TokenTable-ECDSA-Distributor.md
tags:
- firm:codespect
- report:2025-04-23-tokentable-ecdsa-distributor
title: '[I-02] The version information is not included in the signed data.'
vuln_class: []
---

# [I-02] The version information is not included in the signed data.

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-23-TokenTable-ECDSA-Distributor.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-23-TokenTable-ECDSA-Distributor.md)_

---

**Files:** [BaseECDSADistributor.sol](https://github.com/EthSign/ecdsa-token-distributor/tree/6d5db7f144d7468644313c98f9f310dbaadd1b01/src/core/BaseECDSADistributor.sol#L169)

**Description:**

The ECDSADistributor contract is an upgradeable contract and contains version information. After the contract is upgraded, the version information may be changed.

```solidity
function version() public pure virtual override returns (string memory) {
    return "0.4.1";
}
```

However, when constructing the signed data for user claims, the version information is not included in the signature, which may introduce potential risks.

```solidity
function encodeHashToBeSigned(...)
    public
    view
    virtual
    returns (bytes32)
{
    return keccak256(abi.encode(block.chainid, address(this), recipient, userClaimId, userClaimData));
}
```

**Impact:** After the contract version information is changed, previously generated signatures can still be used. This may pose some potential risks.

**Recommendation:** It is recommended to include the version information in the signed data.

**Status:** Acknowledged

**Client response:** Acknowledged

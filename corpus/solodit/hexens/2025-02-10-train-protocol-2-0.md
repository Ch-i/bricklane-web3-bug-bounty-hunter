---
affected_contracts: []
derives_from: []
id: solodit-hexens-2025-02-10-train-protocol-2-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-02-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-02-10-Train-Protocol.md
tags:
- firm:hexens
- report:2025-02-10-train-protocol
title: '[LYSWP2-5] Immutable DOMAIN_SEPARATOR becomes invalid after a hard fork'
vuln_class: []
---

# [LYSWP2-5] Immutable DOMAIN_SEPARATOR becomes invalid after a hard fork

_Section severity (from Solodit section header): Low_  
_Audit firm: Hexens_  
_Source report: [2025-02-10-Train-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-02-10-Train-Protocol.md)_

---

**Severity:** Low

**Description:** The `DOMAIN_SEPARATOR` in the `HashedTimeLockERC20`, `HashedTimeLockEther` contracts are defined as a constant and remains unchanged after contract deployment. However, if a hard fork occurs, the `block.chainid` on one of the forked chains will change. This approach is potentially unsafe as such signatures could be deemed valid in forked networks, thus creating a vulnerability to replay attacks.
```  constructor() {
    DOMAIN_SEPARATOR = hashDomain(
      EIP712Domain({
        name: 'LayerswapV8',
        version: '1',
        chainId: block.chainid,
        verifyingContract: address(this),
        salt: 0x2e4ff7169d640efc0d28f2e302a56f1cf54aff7e127eededda94b3df0946f5c0
      })
    );
  }
```

**Remediation:**  Consider using the implementation from `OpenZeppelin`, which recalculates the domain separator if the current `block.chainid` is not the cached chain ID: 
[openzeppelin-contracts/contracts/utils/cryptography/EIP712.sol at 441dc141ac99622de7e535fa75dfc74af939019c · OpenZeppelin/openzeppelin-contracts](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/441dc141ac99622de7e535fa75dfc74af939019c/contracts/utils/cryptography/EIP712.sol#L22-L23)

**Status:**   Fixed


- - -

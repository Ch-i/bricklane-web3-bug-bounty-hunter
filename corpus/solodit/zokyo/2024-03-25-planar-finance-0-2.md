---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-25-planar-finance-0-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-03-25T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md
tags:
- firm:zokyo
- report:2024-03-25-planar-finance
title: Nonce Verification Missing in `permit` Function
vuln_class: []
---

# Nonce Verification Missing in `permit` Function

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-03-25-Planar Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md)_

---

**Severity**: Medium

**Status**:  Unresolved

**Source**: ./UniswapV2ERC20.sol

**Description**:

The `permit` function does not include a check to verify that the nonce used in the signature is correct and has not been used before. This omission can lead to potential signature replay attacks, where an attacker could reuse a valid signature to perform unauthorized operations.

**Recommendation**:

It is recommended to include a nonce verification step in the permit function to ensure that each nonce is used only once. This can be achieved by checking the current nonce for the owner against the provided nonce in the function call and then incrementing the nonce after a successful verification and approval. 
```solidity
    mapping (address => uint)                      public nonces;
function permit(address owner, address spender, uint value, uint deadline, uint8 v, bytes32 r, bytes32 s, uint nonce) external {
    require(deadline >= block.timestamp, 'UniswapV2: EXPIRED');
    require(nonce == nonces[owner], 'UniswapV2: INVALID_NONCE'); // Nonce verification
    bytes32 digest = keccak256(
        abi.encodePacked(
            '\x19\x01',
            DOMAIN_SEPARATOR,
            keccak256(abi.encode(PERMIT_TYPEHASH, owner, spender, value, nonce, deadline))
        )
    );
    address recoveredAddress = ecrecover(digest, v, r, s);
    require(recoveredAddress != address(0) && recoveredAddress == owner, 'UniswapV2: INVALID_SIGNATURE');
    _approve(owner, spender, value);
    nonces[owner] += 1; // Increment nonce after successful approval
}
```

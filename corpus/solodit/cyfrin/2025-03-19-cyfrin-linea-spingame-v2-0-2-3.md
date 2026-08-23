---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-19-cyfrin-linea-spingame-v2-0-2-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-03-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-19-cyfrin-linea-spingame-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-19-cyfrin-linea-spingame-v2-0
title: Assembly blocks could benefit from `"memory-safe"` annotation
vuln_class: []
---

# Assembly blocks could benefit from `"memory-safe"` annotation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-19-cyfrin-linea-spingame-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-19-cyfrin-linea-spingame-v2.0.md)_

---

**Description:** When hashing request data in [`Spin::_hashParticipation`](https://github.com/Consensys/linea-hub/blob/295344925ec4321265f7cbac174fcf903b529a4e/contracts/src/Spin.sol#L383-L409) and [`Spin::_hashClaim`](https://github.com/Consensys/linea-hub/blob/295344925ec4321265f7cbac174fcf903b529a4e/contracts/src/Spin.sol#L411-L438), inline assembly is used to efficiently compute the hash:
```solidity
assembly {
    let mPtr := mload(0x40)
    mstore(
        mPtr,
        0x4635ca970da82693e235d3cdaa3678d42c6824330c48b4135f080d655e54da78 // keccak256("ClaimRequest(address user,uint256 expirationTimestamp,uint64 nonce,uint32 prizeId)")
    )
    mstore(add(mPtr, 0x20), _user)
    mstore(add(mPtr, 0x40), _expirationTimestamp)
    mstore(add(mPtr, 0x60), _nonce)
    mstore(add(mPtr, 0x80), _prizeId)
    claimHash := keccak256(mPtr, 0xa0)
}
```

To improve compiler optimizations, consider adding a [`memory-safe`](https://docs.soliditylang.org/en/latest/assembly.html#memory-safety) annotation to the assembly block:

```diff
+ assembly ("memory-safe") {
```

Since the assembly block only accesses memory after the free memory pointer (`0x40`), this annotation poses no risk and can allow the Solidity compiler to apply additional optimizations, improving gas efficiency.

**Linea:** Fixed in commit [`b4aaffc`](https://github.com/Consensys/linea-hub/commit/b4aaffc43e496b085e54ef2b08397fcb3c310e68)

**Cyfrin:** Verified.

\clearpage

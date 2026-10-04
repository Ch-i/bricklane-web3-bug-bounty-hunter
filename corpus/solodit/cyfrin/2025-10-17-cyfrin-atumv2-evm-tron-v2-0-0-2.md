---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-17-cyfrin-atumv2-evm-tron-v2-0-0-2
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-10-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-17-cyfrin-atumv2-evm-tron-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-17-cyfrin-atumv2-evm-tron-v2-0
title: Events emitted using `indexed` structs can be harder to query than using simple
  types
vuln_class: []
---

# Events emitted using `indexed` structs can be harder to query than using simple types

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-17-cyfrin-atumv2-evm-tron-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-17-cyfrin-atumv2-evm-tron-v2.0.md)_

---

**Description:** In Atum V1 events were emitted using `indexed` simple types eg:
```solidity
    event Deposited(
        bytes32 indexed requestId,
        bytes32 indexed depositId,
        address indexed depositor,
        address reserver,
        address releaser,
        IERC20 token,
        uint256 amount
    );
```

This made is very easy to query for all deposits belonging to a given `depositor` address.

But in Atum V2 events are now emitted using `indexed` structs:
```solidity
    event Deposited(
        bytes32 indexed depositId, DepositWitness indexed depositWitness, ReserveWitness indexed reserveWitness
    );
```

Now it is much harder to query for all deposits belonging to a given `depositor` address, since when a struct is marked as indexed, it is treated as a complex type. The topic (used for filtering) stores the Keccak-256 hash of a special in-place encoding of the entire struct (concatenation of its members' encodings, padded to multiples of 32 bytes).

To query, you must know the exact values of all fields in the struct to compute the matching hash and filter by it. Partial matches (e.g., filtering by just one field) are impossible using the topic alone—you'd need to fetch broader logs and filter off-chain, which is less efficient.

Consider "unpacking" structs when emitting events and indexing the most important individual basic fields used in queries.

**Atum:**
Acknowledged.

\clearpage

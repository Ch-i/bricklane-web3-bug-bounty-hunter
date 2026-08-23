---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-4-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-04-11T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md
tags:
- firm:cyfrin
- report:2024-04-11-cyfrin-wormhole-evm-ntt-v2
title: Optimize the `TrimmedAmount` struct as a bit-packed `uint72` user-defined type
vuln_class: []
---

# Optimize the `TrimmedAmount` struct as a bit-packed `uint72` user-defined type

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-11-cyfrin-wormhole-evm-ntt-v2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md)_

---

The existing [`TrimmedAmount`](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/libraries/TrimmedAmount.sol#L5-L8) abstraction has a [runtime gas overhead](https://soliditylang.org/blog/2021/09/27/user-defined-value-types/) due to allocation of the struct:
```solidity
struct TrimmedAmount {
    uint64 amount;
    uint8 decimals;
}
```

This could be mitigated by instead implementing a user-defined type that is a bit-packed `uint72` representation of a token amount and its decimals. The use of a `uint72` type ensures that the existing width of 9 bytes is maintained, which allows for tight packing elsewhere in storage, such as in the `RateLimitParams` struct:
```solidity
struct RateLimitParams {
        TrimmedAmount limit;
        TrimmedAmount currentCapacity;
        uint64 lastTxTimestamp;
    }
```
therefore keeping this definition contained within a single word.

Despite the non-trivial refactoring effort required, a user-defined value type is advantageous here as it would allow for the trimmed amounts to be stack-allocated and arithmetic operators to be overloaded.

**Wormhole Foundation:** Fixed in [PR \#248](https://github.com/wormhole-foundation/example-native-token-transfers/pull/248).

**Cyfrin:** Verified. Some comments are incorrect, and further small optimizations could be made, but otherwise appears correct.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-1-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-04-11T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md
tags:
- firm:cyfrin
- report:2024-04-11-cyfrin-wormhole-evm-ntt-v2
title: Silent overflow in `TrimmedAmount::shift` could result in rate limiter being
  bypassed
vuln_class: []
---

# Silent overflow in `TrimmedAmount::shift` could result in rate limiter being bypassed

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-11-cyfrin-wormhole-evm-ntt-v2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md)_

---

**Description:** Within [`TrimmedAmount::trim`](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/libraries/TrimmedAmount.sol#L136-L158), there is an explicit check that ensures the scaled amount does not exceed the maximum `uint64`:
```solidity
// NOTE: amt after trimming must fit into uint64 (that's the point of
// trimming, as Solana only supports uint64 for token amts)
if (amountScaled > type(uint64).max) {
    revert AmountTooLarge(amt);
}
```
However, no such check exists within [`TrimmedAmount::shift`](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/libraries/TrimmedAmount.sol#L121-L129) which means there is potential for silent overflow when casting to `uint64` here:
```solidity
function shift(
    TrimmedAmount memory amount,
    uint8 toDecimals
) internal pure returns (TrimmedAmount memory) {
    uint8 actualToDecimals = minUint8(TRIMMED_DECIMALS, toDecimals);
    return TrimmedAmount(
        uint64(scale(amount.amount, amount.decimals, actualToDecimals)), actualToDecimals
    );
}
```

**Impact:** A silent overflow in `TrimmedAmount::shift` could result in the rate limiter being bypassed, considering its usage in [`NttManager::_transferEntryPoint`](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/NttManager/NttManager.sol#L300). Given the high impact and reasonable likelihood of this issue occurring, it is classified a **MEDIUM** severity finding.

**Recommended Mitigation:** Explicitly check the scaled amount in `TrimmedAmount::shift` does not exceed the maximum `uint64`.

**Wormhole Foundation:** Fixed in [PR \#262](https://github.com/wormhole-foundation/example-native-token-transfers/pull/262).

**Cyfrin:** Verified. OpenZeppelin `SafeCast` library is now used when casting to `uint64`.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-1-8
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: '`DividendManager::distributePayout` will always revert after 255 payouts,
  preventing any future payout distributions'
vuln_class: []
---

# `DividendManager::distributePayout` will always revert after 255 payouts, preventing any future payout distributions

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** `DividendManager::HolderManagementStorage::_currentPayoutIndex` is declared as `uint8`:
```solidity
/// @dev The current index that is yet to be paid out.
uint8 _currentPayoutIndex;
```

`_currentPayoutIndex` is incremented every time `DividendManager::distributePayout` is called:
```solidity
$._payouts[$._currentPayoutIndex++] = PayoutInfo({
    amount: payoutAmount,
    totalSupply: SafeCast.toUint128(totalSupply())
});
```

**Impact:** The maximum value of `uint8` is 255 so `DividendManager::distributePayout` can only be called 255 times; any further calls will always revert meaning no more payout distributions are possible.

**Recommended Mitigation:** If requiring more than 255 payout distributions:
* use a larger size to store `DividendManager::HolderManagementStorage::_currentPayoutIndex`
* change the `uint8` key in this mapping to match the larger size:
```solidity
mapping(address => mapping(uint8 => TokenBalanceChange)) _balanceHistory;
```
* change the `uint256` key in this mapping to match:
```solidity
mapping(uint256 => PayoutInfo) _payouts;
```

Consider using named mappings to explicitly show that these indexes all refer to the same entity, the payout index.

In Solidity a storage slot is 256 bits and an address uses 160 bits. Examining the relevant storage layout of `struct HolderManagementStorage` shows that `_currentPayoutIndex` could be declared as large as `uint56` without using any additional storage slots:
```solidity
IERC20 _stablecoin; // 160 bits
uint8 _stablecoinDecimals; // 8 bits
uint32 _payoutFee; // 32 bits
// 200 bits have been used so 56 bits available in the current storage slot
// _currentPayoutIndex could be declared as large as `uint56` with no
// extra storage requirements
uint8 _currentPayoutIndex;
```

**Remora:** Fixed in commit [f929ff1](https://github.com/remora-projects/remora-smart-contracts/commit/f929ff115f82e76c8eb497ce769792e8de99602b#diff-b6e3759e2288f06f4db11f44b35e7a6398f0301035472704a0479aab4afd9b48R62) by increasing `_currentPayoutIndex` to `uint16` which will be sufficient.

**Cyfrin:** Verified.

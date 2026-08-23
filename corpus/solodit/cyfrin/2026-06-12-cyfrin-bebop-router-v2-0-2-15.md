---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-12-cyfrin-bebop-router-v2-0-2-15
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-12-cyfrin-bebop-router-v2-0
title: '`BebopPmmHelper::_executePmmSwap` does not validate PMM taker transfer commands
  before using the ERC20 approval path'
vuln_class: []
---

# `BebopPmmHelper::_executePmmSwap` does not validate PMM taker transfer commands before using the ERC20 approval path

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-12-cyfrin-bebop-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md)_

---

**Description:** For single PMM orders, the decoded `packed_commands` field controls how `BebopSettlement` expects to receive the taker's token:

```solidity
// external/bebop-settlement/src/libs/Order.sol:68-73
function extractSingleOrderCommands(
    uint256 commands
) internal pure returns (bool takerHasNative, bool makerHasNative, bool takerUsingPermit2){
    takerHasNative = (commands & 0x01) != 0;
    makerHasNative = (commands & 0x02) != 0;
    takerUsingPermit2 = (commands & 0x04) != 0;
}
```

The router decodes this field but discards it:

```solidity
// contracts/base/BebopPmmHelper.sol:62-76
(
    , // expiry
    , // taker_address
    ...
    , // receiver
    , // packed_commands
    uint256 pmmFlags
) = abi.decode(...);

require(taker_token == expectedFromToken && maker_token == expectedToToken, TokenMismatch());
```

`_executePmmSwap` then always approves the PMM and calls settlement through the ERC20 transfer-from-contract path:

```solidity
// contracts/base/BebopPmmHelper.sol:207-212
bytes memory pmmCalldata = bebopPmmCalldata;
uint256 offset = selector == SWAP_SINGLE_SELECTOR ? SWAP_SINGLE_OFFSET : SWAP_AGGREGATE_OFFSET;
_changeCalldata(pmmCalldata, offset, newFromAmount);
_ensureApproval(IERC20(fromToken), bebopPmm, newFromAmount);

(bool success, bytes memory returnData) = bebopPmm.call(pmmCalldata);
```

If the signed PMM order sets `takerHasNative` or `takerUsingPermit2`, settlement expects a different taker transfer mechanism and the PMM call reverts. The router does not reject that unsupported command mode at its own validation boundary.

**Files:**

- `contracts/base/BebopPmmHelper.sol` - `BebopPmmHelper::_decodeSinglePmm`, `BebopPmmHelper::_executePmmSwap`
- `external/bebop-settlement/src/libs/Order.sol` - `Order::extractSingleOrderCommands`

**Impact:** Single PMM orders signed with non-ERC20 taker commands (`takerHasNative` or `takerUsingPermit2`) revert inside the external PMM call instead of being rejected by the router with a typed validation error. The issue affects diagnostics and integration failure handling for unsupported PMM taker command modes.

**Recommended Mitigation:** Either explicitly validate that the decoded `packed_commands` field corresponds to the supported ERC20 taker-transfer mode, or document clearly that `_executePmmSwap` only supports PMM orders whose taker side can be settled from the router's ERC20 approval. The validation can be added alongside the existing token checks in `_decodeSinglePmm`:

```solidity
// After decoding packed_commands:
(bool takerHasNative, , bool takerUsingPermit2) = Order.extractSingleOrderCommands(packed_commands);
require(!takerHasNative && !takerUsingPermit2, UnsupportedTakerCommand());
```

This converts an opaque settlement revert into a clear, diagnosable router error.

**Bebop:** Fixed in commit [9db95bc](https://github.com/bebop-dex/bebop-rfqa/commit/9db95bc2b423d9317c149e90a70ae51565e26367).

**Cyfrin:**
Verified.

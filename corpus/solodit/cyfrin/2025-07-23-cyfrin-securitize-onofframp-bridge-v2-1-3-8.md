---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-3-8
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-07-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1
title: Unused library and struct definitions increase deployment costs and reduce
  code clarity
vuln_class: []
---

# Unused library and struct definitions increase deployment costs and reduce code clarity

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md)_

---

**Description:** The `CCTPMessageLib` library and `CCTPMessage` struct are defined but never used throughout the CCTP integration contracts. In `WormholeCCTPUpgradeable.sol`, the library defines a `CCTPMessage` struct containing `message` and `signature` fields, and the contract imports it with `using CCTPMessageLib for *`. However, the `CCTPBase::redeemUSDC` function manually decodes CCTP messages using `abi.decod
e(cctpMessage, (bytes, bytes))` instead of utilizing the defined struct.

```solidity
function redeemUSDC(bytes memory cctpMessage) internal returns (uint256 amount) {
    (bytes memory message, bytes memory signature) = abi.decode(cctpMessage, (bytes, bytes));
    uint256 beforeBalance = IERC20(USDC).balanceOf(address(this));
    circleMessageTransmitter.receiveMessage(message, signature);
    return IERC20(USDC).balanceOf(address(this)) - beforeBalance;
}
```

The same issue exists in the upstream wormhole SDK's `CCTPBase.sol` file, suggesting this may have been copied without proper cleanup.

**Impact:** The unused code increases deployment gas costs and reduces code maintainability without providing any functional benefit.

**Recommended Mitigation:** Remove the unused `CCTPMessageLib` library and the `using` statement from the contracts:

```diff
- library CCTPMessageLib {
-     struct CCTPMessage {
-         bytes message;
-         bytes signature;
-     }
- }

abstract contract CCTPSender is CCTPBase {
    uint8 internal constant CONSISTENCY_LEVEL_FINALIZED = 15;

-   using CCTPMessageLib for *;

    mapping(uint16 => uint32) public chainIdToCCTPDomain;
```

**Securitize:** Fixed in commit [97e37b](https://bitbucket.org/securitize_dev/bc-securitize-bridge-sc/commits/97e37bed37168bc1ca73fb18f06fbae06161819d).

**Cyfrin:** Verified.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-1-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-07-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1
title: Incorrect address handling for account abstraction wallets in `SecuritizeBridge::bridgeDSTokens`
vuln_class: []
---

# Incorrect address handling for account abstraction wallets in `SecuritizeBridge::bridgeDSTokens`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md)_

---

**Description:** The `SecuritizeBridge.bridgeDSTokens` function assumes that a user's wallet address (`msg.sender`) on the source chain is identical to their desired recipient address on the destination chain. This assumption is incorrect for Account Abstraction (AA) wallets.

Account Abstraction wallets are smart contract-based wallets (e.g., Safe, Argent, ERC-4337 wallets) that, unlike Externally Owned Accounts (EOAs), can have different addresses across different chains for the same logical user.

This occurs because:
- AA wallets are deployed using factory contracts with chain-specific parameters
- Deployment salts, nonces, or factory addresses may differ between chains
- The same user's wallet logic results in different contract addresses on different chains

This creates a security risk where bridged DSTokens may be minted to an uncontrolled address on the destination chain, potentially resulting in permanent loss of funds.

**Impact:** Tokens can be minted to an address that the user cannot control on the destination chain, and investor registration can be tied to the wrong addresses, breaking KYC/AML assumptions.

**Proof of Concept:**
1. User Alice uses a Safe wallet with address `0xAaa...111` on Ethereum
2. Alice calls `bridgeDSTokens` to bridge 1000 DSTokens to Polygon
3. The contract encodes `msg.sender` (`0xAaa...111`) as the destination address
4. On Polygon, Alice's Safe wallet has address `0xBbb...222` (different factory deployment)
5. DSTokens are minted to `0xAaa...111` on Polygon, which Alice cannot access
6. Alice's funds are permanently lost

**Recommended Mitigation:** Add an explicit `destinationWallet` parameter to allow users to specify their destination address:
```solidity
function bridgeDSTokens(
    uint16 targetChain,
    uint256 value,
    address destinationWallet
) external override payable whenNotPaused {
    require(destinationWallet != address(0), "Invalid destination wallet");

    // ... existing validation code ...

    wormholeRelayer.sendPayloadToEvm{value: msg.value} (
        targetChain,
        targetAddress,
        abi.encode(
            investorDetail.investorId,
            value,
            destinationWallet, // ← User-specified destination
            investorDetail.country,
            investorDetail.attributeValues,
            investorDetail.attributeExpirations
        ),
        0,
        gasLimit,
        whChainId,
        msg.sender
    );
}
```

**Securitize:** Acknowledged.

**Cyfrin:** Acknowledged.

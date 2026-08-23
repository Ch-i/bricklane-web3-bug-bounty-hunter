---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-1-11
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: Block number deadline is chain dependent and unreliable across L2s
vuln_class: []
---

# Block number deadline is chain dependent and unreliable across L2s

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** The `SecuritizeOnRamp::subscribe` uses `block.number` as a deadline mechanism to prevent stale transactions:

```solidity
 function subscribe(
        string memory _investorId,
        address _investorWallet,
        string memory _investorCountry,
        uint8[] memory _investorAttributeIds,
        uint256[] memory _investorAttributeValues,
        uint256[] memory _investorAttributeExpirations,
        uint256 _minOutAmount,
        uint256 _liquidityAmount,
        uint256 _blockLimit,
        bytes32 _agreementHash
    )
        public
        whenNotPaused
        onlySecuritizeOnRamp
        nonZeroNavRate
        validateMinSubscriptionAmount(_liquidityAmount)
    {
        if (_blockLimit < block.number) {
            revert TransactionTooOldError();
        }//@audit where this is going to be deployed?
        ...
```

The protocol is intended to be deployed in this chains as evidenced by the `hardhat.config.ts:

```javascript
 networks: {
        sepolia: {
            chainId: 11155111,
            url: process.env.SEPOLIA_RPC_URL ?? '',
            accounts: [process.env.DEPLOYER_PRIV_KEY!].filter((x) => x),
        },
        arbitrum: {
            chainId: 421614,
            // ...
        },
        optimism: {
            chainId: 11155420,
            // ...
        },
        avaxtest: {
            // ...
        },
    },
```

Block production rates differ drastically across this chains:
* Ethereum mainnet: ~12 seconds per block
* Optimism: ~2 seconds per block
* Arbitrum: ~0.25-0.5 seconds per block

**Impact:** A `_blockLimit` value that provides a reasonable time window on Ethereum becomes nearly useless on L2s. Setting `_blockLimit = currentBlock + 300` provides:
* Ethereum: ~1 hour window
* Optimism: ~10 minutes window
* Arbitrum: ~75-150 seconds window

This could lead valid transactions unexpectedly reverting with `TransactionTooOldError()` on L2s if users/backend calculate `_blockLimit` based on Ethereum assumptions

**Recommended Mitigation:** Replace `block.number` with `block.timestamp` for chain-agnostic deadline enforcement.

**Securitize:** Acknowledged; in practice there is no risk as block span is set by our services and we configure that number per blockchain. We do not want to change this for now because it's attached to our backend.

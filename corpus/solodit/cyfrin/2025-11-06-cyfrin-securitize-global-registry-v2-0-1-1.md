---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-06-cyfrin-securitize-global-registry-v2-0-1-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-11-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-06-cyfrin-securitize-global-registry-v2-0
title: Cross-chain incompatibility with `block.number` based timeout mechanism
vuln_class: []
---

# Cross-chain incompatibility with `block.number` based timeout mechanism

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-06-cyfrin-securitize-global-registry-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md)_

---

**Description:** `GlobalRegistryService::addGlobalInvestorWallet` function uses `block.number` to validate transaction freshness through a `blockLimit parameter`:
```solidity
function addGlobalInvestorWallet(
    string calldata id,
    address walletAddress,
    uint256 blockLimit
) external override whenNotPaused onlySelf newWallet(walletAddress) returns (bool) {
    if (blockLimit < block.number) {
        revert TransactionTooOld();
    }
    // ...
}
```

According to the hardhat configuration, this contract is designed to be deployed on multiple chains with vastly different block production rates:
* Ethereum Mainnet - Block time: ~12-14 seconds
* Sepolia (Ethereum testnet) - Block time: ~12-14 seconds
* Arbitrum (chainId: 421614) - Block time: ~0.25 seconds (48-56x faster)
* Optimism (chainId: 11155420) - Block time: ~2 seconds (6-7x faster)
* Avalanche/Fuji (chainId: 43113) - Block time: ~2 seconds (6-7x faster)

The problem is that block production rates vary dramatically across these chains, making block-based time validation inconsistent and unreliable. I an operator signs a pre-approved transaction with `blockLimit = currentBlock + 100`:
* On Ethereum: Valid for ~100 × 13 seconds = ~21 minutes
* On Arbitrum: Valid for ~100 × 0.25 seconds = ~25 seconds
* On Optimism/Avalanche: Valid for ~100 × 2 seconds = ~3.3 minutes

**Impact:** Transactions could revert in one chain and be added in other chains if an investor is adding the same wallet among different chains.

**Recommended Mitigation:** Replace `block.number` with `block.timestamp` for consistent cross-chain behavior.

**Securitize:** Fixed in commits [8f92757](https://github.com/securitize-io/bc-global-registry-service-sc/commit/8f927571c7526817ffe43c5f37d11560e79809d9), [e99c56f](https://github.com/securitize-io/bc-global-registry-service-sc/commit/e99c56fe94f9b41e0680d2318f504fca33be4919), [920e496](https://github.com/securitize-io/bc-global-registry-service-sc/commit/920e4965bb9306203a8251e58c962f4dfff67a3f).

**Cyfrin:** Verified.

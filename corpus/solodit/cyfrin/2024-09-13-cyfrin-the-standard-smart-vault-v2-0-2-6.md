---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-09-13-cyfrin-the-standard-smart-vault-v2-0-2-6
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-09-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md
tags:
- firm:cyfrin
- report:2024-09-13-cyfrin-the-standard-smart-vault-v2-0
title: Potentially incorrect encoding of swap paths
vuln_class: []
---

# Potentially incorrect encoding of swap paths

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md)_

---

**Description:** During fork testing, it became apparent that swap paths should use packed encoding; however, the [existing mocked test suite](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/test/SmartVault.js#L499-L509) does the following:

```javascript
// data about how yield manager converts collateral to USDC, vault addresses etc
await YieldManager.addHypervisorData(
  MockWeth.address, MockWETHWBTCHypervisor.address, 500,
  new ethers.utils.AbiCoder().encode(['address', 'uint24', 'address'], [MockWeth.address, 3000, USDC.address]),
  new ethers.utils.AbiCoder().encode(['address', 'uint24', 'address'], [USDC.address, 3000, MockWeth.address])
)
```

Referring to the [ethers documentation](https://docs.ethers.org/v5/api/utils/hashing/#utils-solidityPack), this shows that `AbiCoder::encode` is the incorrect method for packed encoding. If extended to the real configuration of Hypervisor data for deployed contracts, this would result in all yield deposit functionality reverting due to failed swaps.

**Impact:** Yield deposit functionality would not work due to incorrect configuration of Hypervisor data.

**Recommended Mitigation:** Use tightly packed encoding for swap paths.

**The Standard DAO:** Acknowledged. We are aware that this kind of encoding would not work in production with real routers, but could not figure out how to decode the correct path types in the mock swap router. Will amend the tests & mock swap router if you are aware of a solution.

**Cyfrin:** Acknowledged. The solution would be to use the Uniswap V3 [Path](https://github.com/Uniswap/v3-periphery/blob/main/contracts/libraries/Path.sol) and [BytesLib](https://github.com/Uniswap/v3-periphery/blob/main/contracts/libraries/BytesLib.sol) libraries; however, this additional complexity may not be desired for the mock tests.

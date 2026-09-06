---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-28-cyfrin-securitize-bridge-v2-0-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-10-28T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-28-cyfrin-securitize-bridge-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-28-cyfrin-securitize-bridge-v2-0
title: Make the gas limit configurable
vuln_class: []
---

# Make the gas limit configurable

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-28-cyfrin-securitize-bridge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-28-cyfrin-securitize-bridge-v2.0.md)_

---

**Description:** The `SecuritizeBridge` contract currently uses a fixed (hardcoded) gas limit of 2,500,000 for all cross-chain message transactions through the Wormhole protocol. This value represents the maximum computational units (gas) allowed for the execution of the transaction on the target chain.

While this value works under current implementation, having it as a hardcoded constant makes it difficult to adjust if future upgrades or changes to the contract's functionality require different gas consumption. For example, if the contract's logic is upgraded and requires more computational steps, the current gas limit might become insufficient, requiring a full contract redeployment just to adjust this value.

**Recommended Mitigation:** Make the gas limit configurable by adding an owner-controlled function to update the value. This would allow the protocol administrators to adjust the gas limit if future contract upgrades require different gas consumption, without requiring a full contract redeployment.

Replace:
```solidity
uint256 public constant GAS_LIMIT = 2500_000;
```
with:
```solidity
uint256 public gasLimit;

function setGasLimit(uint256 _gasLimit) external onlyOwner {
    gasLimit = _gasLimit;
}
```

**Securitize:** Fixed in commit [525d86](https://bitbucket.org/securitize_dev/bc-securitize-bridge-sc/commits/525d8626ac53ab6ab38689e36d9d598c0626c90e).

**Cyfrin:** Verified.

\clearpage

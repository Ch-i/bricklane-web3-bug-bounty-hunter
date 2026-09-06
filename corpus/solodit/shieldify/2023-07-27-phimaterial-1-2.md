---
affected_contracts: []
derives_from: []
id: solodit-shieldify-2023-07-27-phimaterial-1-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-07-27T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Shieldify/2023-07-27-PHIMaterial.md
tags:
- firm:shieldify
- report:2023-07-27-phimaterial
title: '[M-03] Centralization Risk in Multiple Places'
vuln_class: []
---

# [M-03] Centralization Risk in Multiple Places

_Section severity (from Solodit section header): Medium_  
_Audit firm: Shieldify_  
_Source report: [2023-07-27-PHIMaterial.md](https://github.com/solodit/solodit_content/blob/main/reports/Shieldify/2023-07-27-PHIMaterial.md)_

---

**Severity**

Medium Risk

**Description**

For `setEmissionLogic` and `setMaterialObject` in `PhiDaily.sol`, it's documented that `emissionLogic` and `materialObject` should be contracts but in reality, the admin can set any address.

With `setTreasuryAddress`, `setMaxClaimed`, `setRoyalityFee` and `setSecondaryRoyalityFee` in `BaseObject.sol` owner can set not validated values which can result in loss of funds for users.

**Location of Affected Code**

File: [`src/PhiDaily.sol`](https://github.com/PHI-LABS-INC/DailyMaterial/blob/355376812ba1e2eeed97d5447c2afea83a3ca8f1/src/PhiDaily.sol)

```solidity
function setEmissionLogic(address _emissionLogic) external onlyOwner {
function setMaterialObject(address _materialObject) external onlyOwner {
```

File: [`src/utils/BaseObject.sol`](https://github.com/PHI-LABS-INC/DailyMaterial/blob/355376812ba1e2eeed97d5447c2afea83a3ca8f1/src/utils/BaseObject.sol)

```solidity
function setTreasuryAddress(address payable newTreasuryAddress) external onlyOwner {
function setMaxClaimed(uint256 tokenId, uint256 newMaxClaimed) public virtual onlyOwner {
function setRoyalityFee(uint256 newRoyalityFee) external onlyOwner {
function setSecondaryRoyalityFee(uint256 newSecondaryRoyalty) external onlyOwner {
```

**Recommendation**

Add proper address validation and upper-bound checks for the fees setter functions despite the fact all these functions are callable only by the owner.

**Team Response**

Acknowledged, Timelock and Multisig will implemented.

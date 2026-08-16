---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-4-6
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Prefer `calldata` to `memory` for external function parameters
vuln_class: []
---

# Prefer `calldata` to `memory` for external function parameters

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** Prefer `calldata` to `memory` for external function parameters:

File: `src/DropBox.sol`:
```solidity
158:  function removeOneTimeCodeToAddress(string memory code, address allowedAddress) external only(apiAddress) {
203:    string memory code,
308:  function revealDropBoxes(string memory code) external payable nonReentrant {
406:  function claimDropBoxes(uint256[] memory _boxIds) external payable nonReentrant {
781:  function getBoxTierAndBlockTsOfIds(uint256[] memory boxIds) external view returns (uint256[3][] memory) {
798:  function getOneTimeCodeData(address sender, string memory code) external view returns (OneTimeCode memory) {
805:  function getOneTimeCodeToAddress(address sender, string memory code) external view returns (address) {
929:  function setContractURI(string memory __contractURI) external onlyOwner {
939:  function setBaseTokenURI(string memory __baseTokenURI) external onlyOwner {
```

**Mode:**
Fixed in commit [9776bc3](https://github.com/Earnft/dropbox-smart-contracts/commit/9776bc3f3be227afb45e22356c9887cd4c428b43) & [b0cc24a](https://github.com/Earnft/dropbox-smart-contracts/commit/b0cc24a8450b21c86c92ee8e0056a89d3f0a80b5).

**Cyfrin:** Verified.

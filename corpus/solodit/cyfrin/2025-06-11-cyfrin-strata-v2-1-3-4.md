---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-3-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-06-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-11-cyfrin-strata-v2-1
title: Prefix internal and private function names with `_` character
vuln_class: []
---

# Prefix internal and private function names with `_` character

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** It is considered good practice in Solidity to prefix internal and private function names with `_` character. This is done sometimes but not other times; ideally apply this consistently:
```solidity
predeposit/PreDepositPhaser.sol
15:    function setYieldPhaseInner () internal {

predeposit/yUSDeDepositor.sol
54:    function deposit_pUSDe (address from, uint256 amount, address receiver) internal returns (uint256) {
62:    function deposit_pUSDeDepositor (address from, IERC20 asset, uint256 amount, address receiver) internal returns (uint256) {

predeposit/PreDepositVault.sol
59:    function onAfterDepositChecks () internal view {
64:    function onAfterWithdrawalChecks () internal view {

predeposit/pUSDeVault.sol
93:    function _deposit(address caller, address receiver, uint256 assets, uint256 shares) internal override {
115:    function _withdraw(address caller, address receiver, address owner, uint256 assets, uint256 shares) internal override {
177:    function stakeUSDe(uint256 USDeAssets) internal returns (uint256) {

predeposit/yUSDeVault.sol
43:    function _convertAssetsToUSDe (uint pUSDeAssets, bool withYield) internal view returns (uint256) {
79:    function _deposit(address caller, address receiver, uint256 pUSDeAssets, uint256 shares) internal override {
86:    function _withdraw(address caller, address receiver, address owner, uint256 pUSDeAssets, uint256 shares) internal override {
101:    function _valueMulDiv(uint256 value, uint256 mulValue, uint256 divValue, Math.Rounding rounding) internal view virtual returns (uint256) {

predeposit/MetaVault.sol
84:    function _deposit(address token, address caller, address receiver, uint256 baseAssets, uint256 tokenAssets, uint256 shares) internal virtual {
160:    ) internal virtual {
175:    function requireSupportedVault(address token) internal view {
191:    function addVaultInner (address vaultAddress) internal {
209:    function removeVaultAndRedeemInner (address vaultAddress) internal {
231:    function redeemMetaVaults () internal {
240:    function redeemRequiredBaseAssets (uint baseTokens) internal {

predeposit/pUSDeDepositor.sol
92:    function deposit_sUSDe (address from, uint256 amount, address receiver) internal returns (uint256) {
102:    function deposit_USDe (address from, uint256 amount, address receiver) internal returns (uint256) {
114:    function deposit_viaSwap (address from, IERC20 token, uint256 amount, address receiver) internal returns (uint256) {
146:    function getPhase () internal view returns (PreDepositPhase phase) {

test/ethena/StakedUSDe.sol
190:  function _checkMinShares() internal view {
203:    internal
225:    internal
239:  function _updateVestingAmount(uint256 newVestingAmount) internal {
251:  function _beforeTokenTransfer(address from, address to, uint256) internal virtual {

test/ethena/SingleAdminAccessControl.sol
72:  function _grantRole(bytes32 role, address account) internal override returns (bool) {
```

**Strata:** Fixed in commit [b154fec](https://github.com/Strata-Money/contracts/commit/b154fec8957a81b3c0cf6e204e894d60bb0d852b).

**Cyfrin:** Verified.

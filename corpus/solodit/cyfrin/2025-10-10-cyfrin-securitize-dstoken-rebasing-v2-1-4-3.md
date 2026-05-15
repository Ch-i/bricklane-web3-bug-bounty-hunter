---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-4-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: In Solidity don't initialize to default values
vuln_class: []
---

# In Solidity don't initialize to default values

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** In Solidity don't initialize to default values:
```solidity
multicall/IssuerMulticall.sol
31:        for (uint256 i = 0; i < data.length; i++) {

service/ServiceConsumer.sol
38:    uint8 public constant ROLE_NONE = 0;

compliance/ComplianceConfigurationService.sol
34:        for (uint i = 0; i < _countries.length; i++) {

compliance/ComplianceServiceRegulated.sol
27:    uint256 internal constant DS_TOKEN = 0;
34:    uint256 internal constant NONE = 0;
718:        uint256 totalLockedTokens = 0;
720:        for (uint256 i = 0; i < investorIssuancesCount; i++) {
815:        uint256 currentIndex = 0;

trust/TrustService.sol
218:        for (uint i = 0; i < _addresses.length; i++) {

compliance/IDSComplianceService.sol
23:    uint256 internal constant NONE = 0;

trust/IDSTrustService.sol
40:    uint8 public constant NONE = 0;

compliance/WalletManager.sol
75:        for (uint i = 0; i < _wallets.length; i++) {
97:        for (uint i = 0; i < _wallets.length; i++) {

compliance/InvestorLockManager.sol
190:        uint256 totalLockedTokens = 0;
191:        for (uint256 i = 0; i < investorLockCount; i++) {

registry/WalletRegistrar.sol
48:        for (uint256 i = 0; i < _wallets.length; i++) {
56:        for (uint256 i = 0; i < _attributeIds.length; i++) {

registry/IDSRegistryService.sol
34:    uint8 public constant NONE = 0;
40:    uint8 public constant PENDING = 0;

registry/RegistryService.sol
43:        for (uint8 index = 0; index < 16; index++) {
74:        for (uint256 i = 0; i < _wallets.length; i++) {
82:        for (uint256 i = 0; i < _attributeIds.length; i++) {
99:        for (uint8 i = 0; i < 4; i++) {

token/DSToken.sol
29:    uint256 internal constant DEPRECATED_OMNIBUS_NO_ACTION = 0;  // Deprecated, kept for backward compatibility

token/TokenLibrary.sol
29:    uint256 internal constant COMPLIANCE_SERVICE = 0;
31:    uint256 internal constant DEPRECATED_OMNIBUS_NO_ACTION = 0; // Deprecated, keep for backwards compatibility
96:        uint256 totalLocked = 0;
97:        for (uint256 i = 0; i < _params._valuesLocked.length; i++) {

swap/SecuritizeSwap.sol
222:        for (uint256 i = 0; i < _investorAttributeIds.length; i++) {

compliance/ComplianceServiceNotRegulated.sol
48:        code = 0;

utils/BulkBalanceChecker.sol
39:        for (uint256 i = 0; i < length; i++) {

utils/MultiSigWallet.sol
61:        for (uint256 i = 0; i < owners_.length; i++) {
113:        for (uint256 i = 0; i < threshold; i++) {
123:        bool success = false;

compliance/LockManager.sol
180:        uint256 totalLockedTokens = 0;
181:        for (uint256 i = 0; i < investorLockCount; i++) {

compliance/IDSWalletManager.sol
26:    uint8 public constant NONE = 0;

bulk/BulkOperator.sol
54:        for (uint256 i = 0; i < addresses.length; i++) {
61:        for (uint256 i = 0; i < data.length; i++) {
80:        for (uint256 i = 0; i < addresses.length; i++) {

utils/TransactionRelayer.sol
191:        bool success = false;
```

**Securitize:** Acknowledged.

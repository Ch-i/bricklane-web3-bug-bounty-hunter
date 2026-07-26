---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-3-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Use named mapping parameters to explicitly note the purpose of keys and values
vuln_class: []
---

# Use named mapping parameters to explicitly note the purpose of keys and values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** Use named mapping parameters to explicitly note the purpose of keys and values:
```solidity
token/TokenLibrary.sol
36:        mapping(address => uint256) walletsBalances;
37:        mapping(string => uint256) investorsBalances;

mocks/TestToken.sol
39:    mapping(address => uint256) balances;
40:    mapping(address => mapping(address => uint256)) allowed;

data-stores/TokenDataStore.sol
27:    mapping(address => mapping(address => uint256)) internal allowances;
28:    mapping(uint256 => address) internal walletsList;
30:    mapping(address => uint256) internal walletsToIndexes;

swap/SecuritizeSwap.sol
43:    mapping(string => uint256) internal noncePerInvestor;

utils/TransactionRelayer.sol
48:    mapping(bytes32 => uint256) internal noncePerInvestor;

utils/MultiSigWallet.sol
46:    mapping(address => bool) isOwner; // immutable state

data-stores/RegistryServiceDataStore.sol
44:        // Ref: https://docs.soliditylang.org/en/v0.7.1/070-breaking-changes.html#mappings-outside-storage
45:        // mapping(uint8 => Attribute) attributes;
48:    mapping(string => Investor) internal investors;
49:    mapping(address => Wallet) internal investorsWallets;
52:     * @dev DEPRECATED: This mapping is no longer used but must be kept for storage layout compatibility in the proxy.
53:     * Do not use this mapping in new code. It will be removed in future non-proxy implementations.
56:    mapping(address => address) internal DEPRECATED_omnibusWalletsControllers;
58:    mapping(string => mapping(uint8 => Attribute)) public attributes;

data-stores/InvestorLockManagerDataStore.sol
24:    mapping(string => mapping(uint256 => Lock)) internal investorsLocks;
25:    mapping(string => uint256) internal investorsLocksCounts;
26:    mapping(string => bool) internal investorsLocked;
27:    mapping(string => mapping(bytes32 => mapping(uint256 => Lock))) internal investorsPartitionsLocks;
28:    mapping(string => mapping(bytes32 => uint256)) internal investorsPartitionsLocksCounts;
29:    mapping(string => bool) internal investorsLiquidateOnly;

data-stores/TrustServiceDataStore.sol
23:    mapping(address => uint8) internal roles;
24:    mapping(string => address) internal entitiesOwners;
25:    mapping(address => string) internal ownersEntities;
26:    mapping(address => string) internal operatorsEntities;
27:    mapping(address => string) internal resourcesEntities;

data-stores/ComplianceConfigurationDataStore.sol
24:    mapping(string => uint256) public countriesCompliances;

data-stores/WalletManagerDataStore.sol
24:    mapping(address => uint8) internal walletsTypes;
25:    mapping(address => mapping(string => mapping(uint8 => uint256))) internal walletsSlots;

data-stores/ServiceConsumerDataStore.sol
23:    mapping(uint256 => address) internal services;

data-stores/LockManagerDataStore.sol
24:    mapping(address => uint256) internal locksCounts;
25:    mapping(address => mapping(uint256 => Lock)) internal locks;

data-stores/ComplianceServiceDataStore.sol
29:    mapping(string => uint256) internal euRetailInvestorsCount;
30:    mapping(string => uint256) internal issuancesCounters;
31:    mapping(string => mapping(uint256 => uint256)) issuancesValues;
32:    mapping(string => mapping(uint256 => uint256)) issuancesTimestamps;
```

**Securitize:** Fixed in commit [6c7bc52](https://github.com/securitize-io/dstoken/commit/6c7bc52d2c0eaacc06c8c6e26a7abfbd69d2edae).

**Cyfrin:** Verified.

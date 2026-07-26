---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-3-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: Standardize `accountId` data type
vuln_class: []
---

# Standardize `accountId` data type

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** The `accountId` uses different data types in different contracts:
* `uint96` in [`GlobalConfiguration::Data`](https://github.com/zaros-labs/zaros-core-audit/blob/de09d030c780942b70f1bebcb2d245214144acd2/src/perpetuals/leaves/GlobalConfiguration.sol#L44)
* `uint128` in [`TradingAccount::Data`](https://github.com/zaros-labs/zaros-core-audit/blob/de09d030c780942b70f1bebcb2d245214144acd2/src/perpetuals/leaves/TradingAccount.sol#L45) and [`TradingAccountBranch::createTradingAccount`](https://github.com/zaros-labs/zaros-core-audit/blob/de09d030c780942b70f1bebcb2d245214144acd2/src/perpetuals/branches/TradingAccountBranch.sol#L219)
* `uint256` in [`AccountNFT`](https://github.com/zaros-labs/zaros-core-audit/blob/de09d030c780942b70f1bebcb2d245214144acd2/src/account-nft/AccountNFT.sol#L18-L22).

**Recommended Mitigation:** Standardize on one data type everywhere.

**Zaros:** We'll use uint128 data type as default, but:
* `uint96` in `GlobalConfiguration::Data` in order to pack the storage values
* `uint256` in AccountNFT to override `ERC721::_update`

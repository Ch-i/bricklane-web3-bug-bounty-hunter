---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-12-itrust-finance-2-7
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2021-06-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md
tags:
- firm:zokyo
- report:2021-06-12-itrust-finance
title: Boolean equality comparison
vuln_class: []
---

# Boolean equality comparison

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2021-06-12-iTrust Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md)_

---

**Description**

-require(bool)(_AdminList[newAddress] == false) (iTrustVaultFactory.sol#70)
-require(bool)(_TrustedSigners[newAddress] == false) (iTrustVaultFactory.sol#83)
-_TrustedSigners[account] == true (iTrustVaultFactory.sol#88)
-_AdminList[account] == true (iTrustVaultFactory.sol#144)
-_VaultStatus[msg.sender] == false (iTrustVaultFactory.sol#148)
-_VaultStatus[vaultAddress] == true (iTrustVaultFactory.sol#152)
-require(bool,string)(_AdminList[msg.sender] == true) (iTrustVaultFactory.sol#156-159)
-require(bool,string)(_AdminList[msg.sender] == true) (iTrustVaultFactory.sol#33)
-require(bool)(vaultFactory.isPaused() == false) (vaults\Vault.sol#439)

**Recommendation**:

Use boolean values directly without equality comparison

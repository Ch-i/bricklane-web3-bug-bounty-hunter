---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-05-24-struct-finance-1-5
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-05-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md
tags:
- firm:zokyo
- report:2023-05-24-struct-finance
title: Missing Input Validation in StructPriceOracle
vuln_class: []
---

# Missing Input Validation in StructPriceOracle

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-05-24-Struct Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-05-24-Struct%20Finance.md)_

---

**Severity**: Low

**Status**: Acknowledged

**Description**

**Note**: Attacker = (Malicious governance)

**Overview**: 

The StructPriceOracle contract is used to fetch the latest price of the given assets using Chainlink's price feed. The contract allows the owner to set or replace sources for the assets. However, the contract does not have proper input validation in the _setAssetsSources function, which allows an attacker to add a malicious asset source and control the price returned by the getAssetPrice function.

**Vulnerability**: 

The vulnerability exists in the _setAssetsSources function, where the contract allows the owner to set or replace sources for the assets without proper input validation. An attacker can add a malicious asset source that returns an incorrect price. This can lead to incorrect valuation of the assets, which can cause severe financial loss to the users.

**Attack Scenario**: 

An attacker can create a malicious asset source that returns an incorrect price. The attacker can then call the _setAssetsSources function with the malicious asset source address and set it as the source for an asset. When the getAssetPrice function is called with the asset address, the malicious asset source will return the incorrect price, which can cause the valuation of the assets to be incorrect. This can lead to financial loss for the users.

**Impact**: 

The impact of this vulnerability can be severe, as a Malicious Owner can manipulate the price of an asset and cause financial loss to the users. This can also affect the valuation of the assets, which can cause further financial loss. The users can lose trust in the platform, and the reputation of the platform can be damaged.

**Recommendation**: 

To mitigate this vulnerability, the contract should have proper input validation in the _setAssetsSources function. The contract should validate that the address of the asset source is a valid Chainlink aggregator address. Additionally, the contract can also implement a whitelist for the asset sources, where the owner can only set the sources from the whitelist. This will prevent the owner from adding a malicious asset source.

**Comment**: The client'll be using a multisig for governance operations initially. So the scenario is very unlikely to happen as the signers will be some of the industry's trusted parties

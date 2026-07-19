---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-0-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Functions are not restricted.
vuln_class: []
---

# Functions are not restricted.

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

1) RadiantOFT.sol: setLpMintComplete(), setMinter(). 
Functions are not restricted, meaning anyone can call and stop the minting or set a minter address. While function setMinter() can be called only once, there are no deployment scripts to verify that the team will call this function right after the deployment. Thus, anyone can call setMinter() before the deployer and become a minter, and anyone can call setLpMintComplete() and stop minting at any time. 
2) ChefIncentivesController.sol: handleActionAfter(). 
The function used to be restricted, so only valid RTokens or LP multiFeeDistribution can be called. However, at a commit 3df651a62b0446ff2113fe3f1a8506e3f7fff0f7 function is not restricted and can be called by anyone.

**Recommendation**: 

Restrict the function, so that only certain addresses with specific role can call them. 

**Post-audit**: 
Functions were removed and the minting system was changed. Now function mint() can be called only once and is called in the deployment script.

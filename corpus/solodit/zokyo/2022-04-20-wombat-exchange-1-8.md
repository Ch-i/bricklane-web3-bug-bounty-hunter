---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-04-20-wombat-exchange-1-8
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2022-04-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-04-20-Wombat%20Exchange.md
tags:
- firm:zokyo
- report:2022-04-20-wombat-exchange
title: In contract Pool.sol at lines 348-350 function assetOf has a misleading naming.
  It receives a token address and returns the address of the IAsset.
vuln_class: []
---

# In contract Pool.sol at lines 348-350 function assetOf has a misleading naming. It receives a token address and returns the address of the IAsset.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-04-20-Wombat Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-04-20-Wombat%20Exchange.md)_

---

**Recommendation**: Consider renaming to addressOfAsset.

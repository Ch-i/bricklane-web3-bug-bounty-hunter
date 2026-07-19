---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-14-paid-ignition-2-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2021-06-14T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Paid%20Ignition.md
tags:
- firm:zokyo
- report:2021-06-14-paid-ignition
title: Pointless return
vuln_class: []
---

# Pointless return

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2021-06-14-Paid Ignition.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Paid%20Ignition.md)_

---

**Description**

IgnitionCore.sol, setPrivAndAutoTxPool() and setQuoteAsset()
IgnitionPools.sol, addTokenToPool(), setRate(), setBaseTier(), setStartDate(), setEndDate(),
setTokenTotalAmount(), transferPool(), setAdminOnPoolToken(), disablePool()
IgnitionaIDO.sol: addWhitelist(), buyTokensQuoteAsset(), buyTokensETH(), recover_token(),
withdrawToken(), withdraw(), redeemTokens()
These functions return boolean value. Though they always return true or revert the
transaction. Thus it makes the return value pointless.

**Recommendation**:

Remove the return interface.

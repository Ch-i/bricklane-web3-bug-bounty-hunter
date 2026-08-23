---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-24-satin-exchange-1-8
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-02-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md
tags:
- firm:trust-security
- report:2023-02-24-satin-exchange
title: TRST-M-9 Users have to lock Satin/$CASH LP in Ve.sol to vote, but they lose
  on fees while doing so
vuln_class: []
---

# TRST-M-9 Users have to lock Satin/$CASH LP in Ve.sol to vote, but they lose on fees while doing so

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-02-24-Satin.Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-24-Satin.Exchange.md)_

---

**Description:**
To get veSatin tokens and be able to vote users are expected to lock Satin/$CASH LP in 
Ve.sol. When this happens, Ve.sol will start accumulating the fees deriving from the 
Satin/$CASH pool but there is no way for users to collect them, unlike in Gauge.sol. This has 
the effect of having fees locked in Ve.sol and can disincentivize users from locking their LP in 
the system.

**Recommended mitigation:**
Add functionality that allows users to withdraw the fees deriving from the LP they locked 
like it’s done in Gauge.sol. Another option is to have an admin function that can collect the 
fees.

**Team response:**
Fixed

**Mitigation Review:**
The proposed fix adds the function `claimFees()` to Ve.sol, which collects the accumulated 
fees from the Satin/$CASH pool and transfers them to the associated bribe. The fees 
destined to a bribe can only be claimed by users that voted for the pool associated with that 
bribe, the Satin/$CASH pool in this scenario. This means that even if the fees are generated 
by the Satin/$CASH LP locked by every user, they can only be claimed by the subset that 
voted for the Satin/$CASH pool.

**Mitigation Review 2:**
The team acknowledges the issue raised by the mitigation review as intended behavior.

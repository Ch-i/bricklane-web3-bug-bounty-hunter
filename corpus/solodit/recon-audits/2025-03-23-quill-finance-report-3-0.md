---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-quill-finance-report-3-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-quill-finance-report
title: '[I-01] Analysis: Suggested Next Steps'
vuln_class: []
---

# [I-01] Analysis: Suggested Next Steps

_Section severity (from Solodit section header): Informational_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Quill_Finance_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md)_

---

**Executive Summary**

No major smart contract risk was identified by my review

Extensive integration risks can be introduced via zappers

And governance has the ability to cause many issues due to misconfiguration, lack of borrow limits and race conditions around config changes

**Misconfig Risk**

An incorrect relation between MCR, CCR and SCR could cause branch shutdowns 

MCR also may need to be adjusted frequently for tokens that have a high volatility

From my research SCR cannot be considered a "real token" as of now as it tends to trade at 1-1 with ETH, while having a substantially smaller market cap, leading me to believe the price is there due to lack of liquidity and trading more so than because it's properly valued

**Lack of Borrow Limits**

Could be "Mango'd", as discussed for SCR, in lack of borrow limits, low collateral assets could be used to over borrow and lock in massive losses to the protocol

It's crucial that conservative caps are established and constantly monitored and updated

**Race Condition Risks**

Griefing from moving the TCR below the CCR

Self-liquidating if MCR is changed or liquidation premiums are changed

Skipping limits and caps by performing these operations around governance

Shutdown can cause immense MEV opportunities

It's crucial that the execution of these functions is done by Governance, a permissioneless execute massively increases risks to all users

**Private Key Risks**

Shutdown into urgent redemptions can be used steal system value (1% premium + Oracle Drift)

**Suggested Next Steps**

Given the updates, changes, economic considerations and need for borrow limits

As well as your plan to add Borrow Limits and Zaps

I believe the best next step is to go through the mitigation review, set everything up and deploy it

Then go through a Security Contest, with:
- Smart Contracts
- Governance Contracts
- Configuration
- Future Configurations

As part of the scope

This will help you secure not just the Software Architecture, but also the deployed bytecode, which massively reduces operational risks


**Suggested Governance Setup**

Multisig -> Timelock -> Changes

Multisig MUST have `onlyOwner` guard:
https://github.com/safe-global/safe-smart-account/blob/main/contracts/examples/guards/OnlyOwnersGuard.sol


Timelock needs to have cancellor setup
Cancellor should be faster than the Multisig as vetoing is generally a safer operation than executing (can be owners of the multi, or another set of signers (even EOAs)

Shutdown is possibly the one function that would require being fast, you may want to enable a Guardian contract that a set of signers can call, allowing them to perform certain operations instantaneously

It's worth noting that shutdown will lead to `urgentRedemptions` causing a high amount of value to be lost to MEV actors, you should ideally plan around this, by performing the redemptions yourself and passing on the collateral to the original depositors, this is non-trivial and requires planning

**Governance Next steps**

Chart out all functions
Chart out the speed that each function needs
Decide if the Multi / Timelock should only be able to perform it
Decide which operations should be even faster


**Economic Suggested Next Steps**

Due to the introduction of borrow limits, as well as the low liquidity environment currently offered by scroll, no "long lasting" economic decision can be fully done

You'll more likely be forced to monitor the chain for available liquidity (which implies safe liquidations that can be performed) and over time will be able to alter caps

The following methodology could be applied to determine if caps are safe enough:
- Take the average liquidity available on chain
- Compute the amount of assets that could be sold before a PREMIUM change in price (where premium is 5% in your code, but that may change)
- These are the amount of assets that can be sold during liquidations while them being profitable (which ensures they will happen)
- Any amount above this may make liquidation unprofitable (or require more risk, making them less likely)
- Cap the borrow limits to these amounts, and monitor their change over time

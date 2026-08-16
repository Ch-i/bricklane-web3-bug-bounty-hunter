---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-19-lyra-finance-3-5
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-01-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md
tags:
- firm:trust-security
- report:2023-01-19-lyra-finance
title: Model-related risks
vuln_class: []
---

# Model-related risks

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-01-19-Lyra Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md)_

---

**Description:**
Although the Black-Scholes-Merton equation is regularly used to price options, the formula 
itself predicts that the “implied volatility for a particular stock would be the same for all strikes 
and maturities” [1]. The Lyra project is aware that this is incorrect [3] and uses the notion of 
an Implied Volatility Surface to account for the true behavior of options, which deviates from 
the Black-Scholes-Merton model.
However, even this may not be enough. One notable criticism comes from Haug and Taleb [2] 
who argue that even with Implied Volatility Surface modifications the model should not be 
used for options pricing since it assumes that the underlying probability distribution of real 
options prices is a Gaussian distribution. This assumption is unlikely to be true and leads to 
“tail risk”. The section “On the Mathematical Impossibility of Dynamic Hedging” is also worth 
reading given that it is a foundational assumption of the Lyra project.
Also, section “Black-Scholes in practice” of the Wikipedia entry [1] outlines a number of risks 
that are not handled by the Black-Scholes-Merton model. In addition to the volatility risk –
which Lyra attempts to hedge using implied volatility surfaces – the section mentions tail risk, 
liquidity risk, gap risk, and incorrect pricing for deep OTM and deep ITM options. 
Given that Lyra’s model for reducing risk leaves out these additional forms of risk there is a 
chance that one or more of them may cause insolvency under the right conditions.
[1] https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model
[2] “Why We Have Never Used the Black-Scholes-Merton Option Pricing Formula” Espen 
Gaarder Haug and Nassim Nicholas Taleb
[3] In section “Volatality Smiles” they say “One of the incorrect assumptions that the BlackScholes model makes is that the implied volatility is constant across all strikes within the same 
expiry” https://docs.lyra.finance/overview/how-does-lyra-work/options-pricing-and-theamm

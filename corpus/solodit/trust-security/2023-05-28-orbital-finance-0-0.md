---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-28-orbital-finance-0-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-05-28T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md
tags:
- firm:trust-security
- report:2023-05-28-orbital-finance
title: TRST-H-1 A malicious operator can drain the vault funds in one transaction
vuln_class: []
---

# TRST-H-1 A malicious operator can drain the vault funds in one transaction

_Section severity (from Solodit section header): High_  
_Audit firm: Trust Security_  
_Source report: [2023-05-28-Orbital Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md)_

---

**Description:**
The vault operator can swap tokens using the `trade()` function. They pass the following 
structure for each trade:
```solidity
         struct tradeInput { 
             address spendToken;
               address receiveToken;
                 uint256 spendAmt;
                   uint256 receiveAmtMin;
                address routerAddress;
         uint256 pathIndex;
         }
```
Notably, **receiveAmtMin** is used to guarantee acceptable slippage. An operator can simply 
pass 0 to make sure the trade is executed. This allows an operator to steal all the funds in the 
vault by architecting a sandwich attack. 
1. Flashloan a large amount of funds
2. Skew the token proportions in a pool which can be used for trading, by almost 
completely depleting the target token.
3. Perform the trade at >99% slippage
4. Sell target tokens for source tokens on the manipulated pool, returning to the original 
ratio.
5. Pay off the flashloan, and keep the tokens traded at 99% slippage.
In fact, this attack can be done in one TX, different to most sandwich attacks.

**Recommended Mitigation:**
The contract should enforce sensible slippage parameters.

**Team response:**
"Added Chainlink Interface to allow for off-chain price knowledge, in a new contract, 
ChainlinkInterface.sol, which is deployed by the VaultManager at deploy time, and ownership 
is given to the protocol owner. This contract has an "addPriceFeed" function, on per token 
basis. All feeds are assumed to be in USD units. Then, the function "getMinReceived", performs 
the needed math to get the min expected back from a trade. This function is called by the 
VaultManager at trade time, which then checks against the caller's minReceived input. 
Additionally, a slippage for a given pair is now get and set by the AuxInfo.sol contract.

**Mitigation review:**
The integration with Chainlink oracle introduces new issues. There is no check for a stale price 
feed, which makes trading possibly incur high slippage costs. 
```solidity
               (,int priceFromInt,,,) = AIFrom.latestRoundData();
         (,int priceToInt,,,) = AITo.latestRoundData();
```
Additionally, when the contracts are deployed on L2, there is a sequencer down-time issue, 
as detailed here(https://docs.chain.link/data-feeds/l2-sequencer-feeds). The contract should check the sequencer is up when deployed on L2.

**Team Response:**
"Stale price feed check added ChainlinkInterface.sol, "getMinReceived" function, lines 90 - 94. 
Sequencer uptime check added to "getMinReceived" function, line 76."

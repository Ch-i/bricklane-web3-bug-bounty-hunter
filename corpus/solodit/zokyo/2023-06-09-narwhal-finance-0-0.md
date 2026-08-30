---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-0-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: First depositor can break minting of shares
vuln_class: []
---

# First depositor can break minting of shares

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: High

**Status**: Resolved

**Description**

The first depositor of an TradingVaultV2 can maliciously manipulate the share price by depositing the lowest possible amount of liquidity and then artificially inflating the currentBalanceUSDT value.
Attacker deposit (NarwhalTradingVault.deposit) 1 wei of USDT, minting 1 share. They receive 1e18 (1 wei) shares.
Attacker calls NarwhalTrading.openTrade, as a result of the calls chain the NarwhalTradingVault.currentBalanceUSDT value  increases to 100e18 + 1. 
Victim deposits 200e18 USDT. Due to a rounding issue in the inflated vault, they receive only 1 share.
Attacker withdraws their 1 share, which is now worth 150 USDT.

**Recommendation**:

Uniswap V2 solved this issue by sending the first 1000 LP tokens to the zero address. The same can be done in this case i.e. when totalSupply() == 0, mint the first min liquidity LP tokens to the zero address to enable share dilution.
Ensure the number of shares to be minted is non-zero: require(_shares != 0, "zero shares minted");

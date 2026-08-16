---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-quill-finance-report-1-15
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-quill-finance-report
title: '[L-16] Addresses'
vuln_class: []
---

# [L-16] Addresses

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Quill_Finance_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md)_

---

All addresses sourced from:
https://github.com/subvisual/quill/blob/a7c93057ce2de13a27a774f22bddd63878c9fe18/contracts/src/scripts/DeployQuillSCrollMainnet.s.sol#L64-L68

```solidity
    struct TroveManagerParams {
        uint256 CCR;
        uint256 MCR;
        uint256 SCR;
        uint256 LIQUIDATION_PENALTY_SP;
        uint256 LIQUIDATION_PENALTY_REDISTRIBUTION;
        uint256 MIN_DEBT;
        uint256 SP_YIELD_SPLIT;
        uint256 minAnnualInterestRate;
    }
```

```solidity
        TroveManagerParams[] memory troveManagerParamsArray = new TroveManagerParams[](4);
        troveManagerParamsArray[0] = TroveManagerParams(140e16, 110e16, 110e16, 5e16, 10e16, 500e18, 75e16, 6 * _1pct); // WETH
        troveManagerParamsArray[1] = TroveManagerParams(160e16, 120e16, 120e16, 5e16, 10e16, 500e18, 75e16, 6 * _1pct); // wstETH
        troveManagerParamsArray[2] = TroveManagerParams(160e16, 120e16, 120e16, 5e16, 10e16, 500e18, 75e16, 6 * _1pct); // weETH
        troveManagerParamsArray[3] = TroveManagerParams(160e16, 120e16, 120e16, 5e16, 30e16, 500e18, 75e16, 7 * _1pct); // SCROLL
```
--------

20% MCR for wstETH | weETH and SCROLL

120 MCR for wstETH looks crazy - What a loss of efficiency for close to zero advantage

weETH -> Need to research further

--------


120% on Scroll looks somewhat scary on the worst days
25% price change in about 1 day
So arguably there can be a few days where the protocol get's rekt by this

---------

```solidity

    IWETH weth = IWETH(0x5300000000000000000000000000000000000004);
    IERC20Metadata wsteth = IERC20Metadata(0xf610A9dfB7C89644979b4A0f27063E9e7d7Cda32);
    IERC20Metadata weeth = IERC20Metadata(0x01f0a31698C4d065659b9bdC21B3610292a1c506);
    IERC20Metadata scroll = IERC20Metadata(0xd29687c813D741E2F938F4aC377128810E217b1b);

    // https://data.chain.link/feeds/scroll/mainnet/eth-usd
    address eth_usd_oracle = 0x6bF14CB0A831078629D993FDeBcB182b21A8774C;

   // wstETH steth (exchange rate) | Rate arb??
// https://data.chain.link/feeds/scroll/mainnet/wsteth-steth%20exchangerate
    address wsteth_steth_oracle = 0xE61Da4C909F7d86797a0D06Db63c34f76c9bCBDC;

// Exchange rate
// https://data.chain.link/feeds/scroll/mainnet/weeth-eeth-exchange-rate
    address weeth_eth_oracle = 0x57bd9E614f542fB3d6FeF2B744f3B813f0cc1258;


// https://data.chain.link/feeds/scroll/mainnet/scr-usd
    address scroll_usd_oracle = 0x26f6F7C468EE309115d19Aa2055db5A74F8cE7A5;

// NOTE: No page for this??
// https://scrollscan.com/address/0x45c2b8C204568A03Dc7A2E32B71D67Fe97F908A9#readContract
    address chainlinkScrollSequencerUptimeFeed = 0x45c2b8C204568A03Dc7A2E32B71D67Fe97F908A9;


// TODO: Check uptime?
    uint256 eth_usd_stalenessThreshold = _48_HOURS;
    uint256 wsteth_steth_stalenessThreshold = _48_HOURS;
    uint256 weeth_eth_stalenessThreshold = _48_HOURS;
    uint256 scroll_usd_stalenessThreshold = _48_HOURS;

```

**Sequencer Feed**

4/9 Multi can DOS it

https://scrollscan.com/address/0xDce20610907bf67D97d0ECcF31C50eaec73bC034#readProxyContract

**Tokens on Scroll**

wstETH
https://scrollscan.com/address/0xf610a9dfb7c89644979b4a0f27063e9e7d7cda32


WETH
https://scrollscan.com/token/0x5300000000000000000000000000000000000004

SCR
https://scrollscan.com/token/0xd29687c813d741e2f938f4ac377128810e217b1b

weETH
https://scrollscan.com/token/0x01f0a31698c4d065659b9bdc21b3610292a1c506

---

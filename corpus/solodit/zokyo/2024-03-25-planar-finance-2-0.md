---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-25-planar-finance-2-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-03-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md
tags:
- firm:zokyo
- report:2024-03-25-planar-finance
title: Optimizing Gas Usage in Smart Contracts with Caching Techniques
vuln_class: []
---

# Optimizing Gas Usage in Smart Contracts with Caching Techniques

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-03-25-Planar Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md)_

---

**Severity**: Informational

**Status**:  Unresolved

**Locations**: 
BalanceFetcher.sol, line 22
DividendsV2.sol, line 278
FairAuction.sol, line 288
Multicall.sol, line 14
Multicall2.sol, line 22, line 57
PlanarLiquidityPoolRouter.sol, line 228, 242
Presale.sol, line 270
Refund.sol, line 41
UniswapInterfaceMulticall.sol, line 30
Uniswapv2library.sol, line 48

**Description**:

When executing smart contracts, especially on networks where transaction costs can be significant, it's crucial to optimize for gas efficiency. A common inefficiency arises during iterations, where accessing the length property of an array multiple times within a loop can lead to unnecessary gas consumption. This occurs because each retrieval of the array's length is a state access that costs gas.
In the provided example, the function getBalances iterates over an array of token addresses to fetch the balance of each token for a given owner. The inefficiency stems from repeatedly accessing _tokens.length within the loop condition.

**Solution:**

A more gas-efficient approach involves caching the array's length outside of the loop. By storing the length in a local variable before entering the loop, the contract only pays for a single state access, regardless of the number of iterations. This modification can significantly reduce gas costs for transactions, particularly for functions that are called frequently or iterate over large arrays.
```solidity
function getBalances(address _owner, address[] calldata _tokens) external view returns (uint256[] memory balances) {
    uint256 length = _tokens.length; // Cache the length
    balances = new uint256[](length);

    for(uint256 i = 0; i < length; i++) { // Use cached length
        if(!isContract(_tokens[i])) {
            continue;
        }
        try IERC20(_tokens[i]).balanceOf(_owner) returns(uint256 balance) {
            balances[i] = balance;
        } catch {}
    }
}
```

This technique ensures the function is optimized for gas efficiency without compromising functionality. It's a simple yet effective way to reduce the gas cost of loops that access array lengths or similar repeatable state reads.

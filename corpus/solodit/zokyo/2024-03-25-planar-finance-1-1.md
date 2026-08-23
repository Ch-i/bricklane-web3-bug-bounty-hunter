---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-25-planar-finance-1-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-03-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md
tags:
- firm:zokyo
- report:2024-03-25-planar-finance
title: Lack of `accountHash` check in `isContract` function
vuln_class: []
---

# Lack of `accountHash` check in `isContract` function

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-03-25-Planar Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md)_

---

**Severity**: Low

**Status**:  Unresolved

**Source**: BalanceFetcher.sol

**Description**: 

The `isContract` function, as currently implemented, checks if an address contains code by examining the size of the code at that address. This method, however, can yield misleading results due to specific Ethereum Virtual Machine (EVM) behaviors. Specifically:

During contract creation, the contract's code is not yet stored at the address, resulting in `isContract` returning false even for addresses that will imminently hold contract code.
If a contract was previously deployed at an address and then self-destructed, the code size check would return false, disregarding the historical presence of a contract.
Addresses where contracts will be deployed in the future but currently hold no code will also result in a false return value.

**Recommendation**:

To address these limitations and improve the reliability of contract detection, it's recommended to use the extcodehash function instead. This approach considers the hash of the code at an address, which provides a more accurate indication of whether the address is a contract, including for contracts in creation and addresses of destroyed contracts.

```
/**
 * @dev Returns true if `account` is a contract.
 *
 * [IMPORTANT]
 * ====
 * It is unsafe to assume that an address for which this function returns
 * false is an externally-owned account (EOA) and not a contract.
 *
 * Among others, `isContract` will return false for the following
 * types of addresses:
 *
 *  - an externally-owned account
 *  - a contract in construction
 *  - an address where a contract will be created
 *  - an address where a contract lived, but was destroyed
 * ====
 */
function isContract(address account) internal view returns (bool) {
    // According to EIP-1052, 0x0 is the value returned for not-yet created accounts
    // and 0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470 is returned
    // for accounts without code, i.e. `keccak256('')`
    bytes32 codehash;
    bytes32 accountHash = 0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470;
    // solhint-disable-next-line no-inline-assembly
    assembly {
        codehash := extcodehash(account)
    }
    return (codehash != accountHash && codehash != 0x0);
}

```
**Note#6** : It's a read-only contract intended for frontend only. As long as it returns data of a limited static list of contracts, we think it's okay to keep it as is.

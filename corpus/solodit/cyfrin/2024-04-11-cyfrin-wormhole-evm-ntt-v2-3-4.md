---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-3-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-04-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md
tags:
- firm:cyfrin
- report:2024-04-11-cyfrin-wormhole-evm-ntt-v2
title: Multiple `staticcall` success booleans are not checked
vuln_class: []
---

# Multiple `staticcall` success booleans are not checked

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-11-cyfrin-wormhole-evm-ntt-v2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md)_

---

The success boolean returned when performing a `staticcall` on the given ERC20 token is not currently checked for any of the instances. It is understood this is a trust assumption in that legitimate implementations should always have `IERC20::decimals` implemented and should not revert when calling `IERC20::balanceOf`; however, it is recommended to check this returned value so as to guarantee the impossibility of erroneously using the revert data when expecting to decode something else.

```solidity
function _getTokenBalanceOf(
    address tokenAddr,
    address accountAddr
) internal view returns (uint256) {
    (, bytes memory queriedBalance) =
        tokenAddr.staticcall(abi.encodeWithSelector(IERC20.balanceOf.selector, accountAddr));
    return abi.decode(queriedBalance, (uint256));
}
```

**Wormhole Foundation:** Fixed in [PR \#375](https://github.dev/wormhole-foundation/example-native-token-transfers/pull/375).

**Cyfrin:** Verified. The success booleans are now checked.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-wannabetv2-v2-0-0-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-wannabetv2-v2-0
title: Owner of `BetFactory` can subtly rug-pull any caller to `BetFactory::createBet`
  stealing their tokens
vuln_class: []
---

# Owner of `BetFactory` can subtly rug-pull any caller to `BetFactory::createBet` stealing their tokens

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-wannabetv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md)_

---

**Description:** Owner of `BetFactory` can rug-pull any caller to `createBet` stealing their tokens by front-running to call `BetFactory::setPool` with the address of a malicious contract that implements the same interface as Aave `supply` function and just transfers tokens to itself.

This works since `Bet::initialize` gives max approval to the pool then calls the `supply` function on it:
```solidity
// If the pool is set, approve and supply the funds to the pool
if (pool != address(0)) {
    IERC20(initialBet.asset).approve(pool, type(uint256).max);

    _aavePool.supply(
        initialBet.asset,
        initialBet.makerStake,
        address(this),
        0
    );
}
```

**Recommended Mitigation:** In `BetFactory::createBet,predictBetAddress` include `tokenToPool[asset]` in the salt passed to `Clones.cloneDeterministic`. This way if it has changed the new `Bet` contract will be created at a different address which the caller has not approved, the first token transfer in `Bet::initialize` will revert causing the entire transaction to revert.

The recommended fix for I-9 also resolves this issue, since it prevents the owner from setting the Aave pool associated with a token to an illegitimate pool.

**WannaBet:** Initially we fixed this in commit [fbd8016](https://github.com/gskril/wannabet-v2/commit/fbd80169eebe70ce96a0ddbbe61035014ee0b018) by including the aave pool in the salt. But after implementing the fixes for I-9 (pool validation) in commit [70e1565](https://github.com/gskril/wannabet-v2/commit/70e1565b391992b7ea8b11f2cc59195478a69212) we no longer included the pool in the salt since the pool can only be set to a valid one.

**Cyfrin:** Verified.

\clearpage

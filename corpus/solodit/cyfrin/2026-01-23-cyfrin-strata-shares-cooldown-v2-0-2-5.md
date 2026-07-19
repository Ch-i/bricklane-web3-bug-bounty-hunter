---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-23-cyfrin-strata-shares-cooldown-v2-0-2-5
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-01-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-23-cyfrin-strata-shares-cooldown-v2-0
title: sUSDe withdrawals can be blocked by receiver restrictions
vuln_class: []
---

# sUSDe withdrawals can be blocked by receiver restrictions

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md)_

---

**Description:** Finalization paths that attempt to deliver `sUSDe` to the user can revert if the receiver is in `FULL_RESTRICTION MODE`. The [sUSDe token](https://etherscan.io/token/0x9d39a5de30e57443bff2a8307a4256c8797a3497#code) enforces transfer restrictions via `_beforeTokenTransfer`, which blocks transfers from or to addresses with `FULL_RESTRICTED_STAKER_ROLE`, causing sUSDe-based finalization during SharesCooldown to revert.
```solidity
/**
   * @dev Hook that is called before any transfer of tokens. This includes
   * minting and burning. Disables transfers from or to of addresses with the FULL_RESTRICTED_STAKER_ROLE role.
   */

  function _beforeTokenTransfer(address from, address to, uint256) internal virtual override {
    if (hasRole(FULL_RESTRICTED_STAKER_ROLE, from) && to != address(0)) {
      revert OperationNotAllowed();
    }
    if (hasRole(FULL_RESTRICTED_STAKER_ROLE, to)) {
      revert OperationNotAllowed();
    }
  }
```

A realistic scenario is that the user is not restricted at the time of `requestRedeem`, but becomes restricted during the cooldown period; once the cooldown expires, any attempt to finalize in `sUSDe` fails. As a result, the user is effectively forced to finalize through `USDe`, incurring an additional unstake cooldown and altering the expected exit behavior.

**Recommended Mitigation:** The protocol should account for potential sUSDe restriction changes at finalization time

**Strata:** **Cyfrin:**

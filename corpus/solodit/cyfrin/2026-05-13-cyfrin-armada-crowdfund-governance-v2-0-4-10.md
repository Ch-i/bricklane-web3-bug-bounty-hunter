---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-4-10
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: Optimize away redundant external calls by adding combined helpers
vuln_class: []
---

# Optimize away redundant external calls by adding combined helpers

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** Several sites issue multiple external calls to the same target contract where a combined helper would reduce to one CALL (~700 gas warm each, plus the duplicate SLOADs the secondary getter performs).

1. **`TreasurySteward::currentSteward, isStewardActive`** - `ArmadaGovernor` makes both calls at 3 sites: `proposeStewardSpend` at `contracts/governance/ArmadaGovernor.sol:688-689`, `queue` Steward branch at `:913-919`, `execute` Steward branch at `:953-959`. The second call re-reads `currentSteward` from storage; its own `currentSteward != address(0)` clause is also always true when reached from these callers (the preceding `msg.sender == currentSteward` / `p.proposer == currentSteward` check pins it non-zero).

2. **`ArmadaToken::totalSupply, balanceOf`** - `ArmadaRedemption::circulatingSupply` at `contracts/governance/ArmadaRedemption.sol:196-203` makes 5 calls (1 totalSupply + 4 balanceOf) per `redeem`; a batch-aware view collapses to 1.

3. **`ArmadaToken::transfer, delegateOnBehalf`** - paired at `RevenueLock::release` at `contracts/governance/RevenueLock.sol:162-163` and `ArmadaCrowdfund::_processClaim` at `contracts/crowdfund/ArmadaCrowdfund.sol:510-511`. A combined `transferAndDelegate` entry collapses to 1.

**Recommended Mitigation:** Add combined entry points to the target contracts:

```solidity
// TreasurySteward.sol
function getCurrentSteward() external view returns (address steward, bool isActive) {
    steward = currentSteward;
    isActive = steward != address(0) && block.timestamp < termStart + TERM_DURATION;
}

// ArmadaToken.sol
function circulatingSupplyOf(address[] calldata excluded) external view returns (uint256 result) {
    result = totalSupply();
    for (uint256 i; i < excluded.length; i++) {
        result -= balanceOf(excluded[i]);
    }
}

function transferAndDelegate(address to, uint256 amount, address delegatee) external returns (bool ok) {
    require(authorized[msg.sender], "ArmadaToken: not authorised");
    ok = transfer(to, amount);
    require(ok, "ArmadaToken: transfer failed");
    _delegate(to, delegatee);
}
```

In `ArmadaGovernor::queue, execute`, lift `stewardContract == address(0)` out of the existing OR-chain at `:914`, `:954` so the external call is skipped when the contract is unset; consume the tuple from `getCurrentSteward()` in one call. In `ArmadaRedemption::redeem` and `RevenueLock::release` / `ArmadaCrowdfund::_processClaim`, replace the multi-call sequences with the combined entry.

**Armada:** Fixed in commit [520fc99](https://github.com/ship-armada/armada-poc/commit/520fc990787364527818500c58ff9c4ce8910937).

**Cyfrin:** Verified.


\clearpage

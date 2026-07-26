---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-0-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: Critical
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: Any staker can fully avoid slashing by triggering OOG reverts
vuln_class: []
---

# Any staker can fully avoid slashing by triggering OOG reverts

_Section severity (from Solodit section header): Critical_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** The finding is similar to [*Malicious actors can force vaults to exit if they wish to get rewards*](#malicious-actors-can-force-vaults-to-exit-if-they-wish-to-get-rewards), but actually different (different fix, different impact, similarity is iterating over the vaults to trigger OOG).

Upon slashing, we calculate the redeemable rewards for the account to slash by going over all of the account vaults and summing them up:
```solidity
for (uint256 i = 0; i < accountVaults.length; i++) {
    accountTotalRewards += rewardsBalanceOf(accountVaults[i]);
}
```
The issue is that the account can register a ton of vaults using `VaultFactory::createVault()`:
```solidity
function createVault() external returns (StakeVault clone) {
    clone = StakeVault(Clones.clone(vaultImplementation));
    clone.initialize(msg.sender, stakeManager);
    clone.register();
    emit VaultCreated(address(clone), msg.sender);
}
````

This will cause the loop to go OOG, thus it is impossible to slash that account.

**Impact:** Slashes are made impossible.

**Recommended Mitigation:** Consider having a sensible limit on the vaults an account can register, i.e. 10.

**StatusL2:** Fixed in [6697432](https://github.com/status-im/status-network-monorepo/commit/6697432b862ee515d1783941a78d07e9a91991eb).

**Cyfrin:** Verified.

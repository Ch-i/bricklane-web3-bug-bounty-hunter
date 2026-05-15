---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-4-6
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: '`Karma::removeRewardDistributor` burns all virtual Karma'
vuln_class: []
---

# `Karma::removeRewardDistributor` burns all virtual Karma

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** Admin can remove reward distributor from `Karma.sol`, this function burns full balance:
```solidity
    function _removeRewardDistributor(address distributor) internal virtual {
        if (!rewardDistributors.contains(distributor)) {
            revert Karma__UnknownDistributor();
        }
@>      _burn(distributor, super.balanceOf(distributor));
        rewardDistributors.remove(distributor);
    }
```

Problem is that not all tokens belong to reward distributor, at least part of them is unclaimed rewards belonging to users. Such tokens can be claimed via `redeemRewards` for example in `SimpleKarmaDistributor.sol`:
```solidity
    function redeemRewards(address account) external returns (uint256) {
@>      uint256 amount = balances[account];
        if (amount == 0) {
            return 0;
        }

        balances[account] = 0;
        mintedSupply -= amount;

@>      karmaToken.safeTransfer(account, amount);

        return amount;
    }
```



**Recommended Mitigation:** `Karma::removeRewardDistributor` is supposed to be used during emergency. In that case distributor can report incorrect virtual Karma, so it's unreliable to leave those virtual karma on balance. That's why it's burned currently.

Consider documenting this behaviour. Additionally if removing burns virtual Karma belonging to users, you should reimburse it to users via `KarmaAirdrop.sol` or direct mint.

**StatusL2:** Fixed in [19557eb](https://github.com/status-im/status-network-monorepo/commit/19557eb034dbb532c745fd910d6dd2e2a26ab9ee).

**Cyfrin:** Verified.

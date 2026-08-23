---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-4-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: The `savedProfit` mapping will always return zero
vuln_class: []
---

# The `savedProfit` mapping will always return zero

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** When a DAO member calls [`MembershipERC1155::claimProfit`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/tokens/MembershipERC1155.sol#L138-L147), their current profit is calculated in []([`MembershipERC1155::saveProfit`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/tokens/MembershipERC1155.sol#L178-187):)

```solidity
function saveProfit(address account, address currency) internal returns (uint profit) {
    uint unsaved = getUnsaved(account, currency);
    lastProfit[account][currency] = totalProfit[currency];
    profit = savedProfit[account][currency] + unsaved;
    savedProfit[account][currency] = profit;
}
```

Here, `savedProfit` is incremented by the calculated unsaved profit. The profit is then paid in `MembershipERC1155::claimProfit` after resetting `savedProfit` to zero:

```solidity
function claimProfit(address currency) external returns (uint profit) {
    profit = saveProfit(msg.sender, currency);
    require(profit > 0, "No profit available");
    savedProfit[msg.sender][currency] = 0;
    IERC20(currency).safeTransfer(msg.sender, profit);
    emit Claim(msg.sender, profit);
}
```

Since `savedProfit` is reset to zero within the lifetime of the same call in which it is initialized, the mapping will always return `0` for a given currency/member pair. Thus, usage in the `savedProfit[account][currency] + unsaved` [expression](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/tokens/MembershipERC1155.sol#L185) is redundant, meaning the value stored in `savedProfit` is never used and can be safely removed.

**Recommended Mitigation:** Consider removing `savedProfit`.

**One World Project:** Updated usage for savedProfit mapping in [`a3980c1`](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/commit/a3980c17217a0b65ecbd28eb078d4d94b4bd5b80)

**Cyfrin:** Closed. `savedProfit` now used.

\clearpage

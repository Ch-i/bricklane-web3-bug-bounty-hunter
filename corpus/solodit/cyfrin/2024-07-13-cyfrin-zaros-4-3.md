---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-4-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: Move immutable branch check outside `for` loop in `RootUpgrade::removeBranch`
vuln_class: []
---

# Move immutable branch check outside `for` loop in `RootUpgrade::removeBranch`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** Move immutable branch check outside `for` loop in `RootUpgrade::removeBranch` - this check should only occur once not during every loop iteration.

**Recommended Mitigation:**
```solidity
function removeBranch(Data storage self, address branch, bytes4[] memory selectors) internal {
    if (branch == address(this)) {
        revert Errors.ImmutableBranch();
    }

    for (uint256 i = 0; i < selectors.length; i++) {
        bytes4 selector = selectors[i];
        // also reverts if left side returns zero address
        if (selector == bytes4(0)) {
            revert Errors.SelectorIsZero();
        }
        if (self.selectorToBranch[selector] != branch) {
            revert Errors.CannotRemoveFromOtherBranch(branch, selector);
        }

        delete self.selectorToBranch[selector];
        // slither-disable-next-line unused-return
        self.branchSelectors[branch].remove(selector);
        // if no more selectors in branch, remove branch address
        if (self.branchSelectors[branch].length() == 0) {
            // slither-disable-next-line unused-return
            self.branches.remove(branch);
        }
    }
}
```

**Zaros:** Fixed in commit [6313b3f](https://github.com/zaros-labs/zaros-core/commit/6313b3f2b485e244679b23f937e66b0144e59f31).

**Cyfrin:** Verified.

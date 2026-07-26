---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-13-cyfrin-safe-harbor-v2-0-1-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-01-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-13-cyfrin-safe-harbor-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-13-cyfrin-safe-harbor-v2-0
title: '`Agreement::removeAccounts` can leave chain with zero accounts'
vuln_class: []
---

# `Agreement::removeAccounts` can leave chain with zero accounts

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-13-cyfrin-safe-harbor-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-13-cyfrin-safe-harbor-v2.0.md)_

---

**Description:** When creating or modifying chains via `Agreement::addChains`, `Agreement::addOrSetChains`, the `Agreement::_validateChains` function enforces that each chain must have at least one account:

```solidity
function _validateChains(Chain[] memory _chains) internal {
    for (uint256 i = 0; i < _chains.length; i++) {
        // ...
        if (_chains[i].accounts.length == 0) { //@audit does not allow chain with zero accounts
            revert Agreement__ZeroAccountsForChainId(_chains[i].caip2ChainId);
        }
        // ...
    }
}
```

However, `Agreement::removeAccounts` does not check whether removal would leave zero accounts:

```solidity
function removeAccounts(string memory _caip2ChainId, string[] memory _accountAddresses) external onlyOwner {
    if (!_chainExists(_caip2ChainId)) {
        revert Agreement__ChainNotFoundByCaip2Id(_caip2ChainId);
    }
    // @audit No check for remaining accounts after removal
    for (uint256 i = 0; i < _accountAddresses.length; i++) {
        uint256 accountIndex = _findAccountIndex(_caip2ChainId, _accountAddresses[i]);
        emit AccountRemoved(_caip2ChainId, _accountAddresses[i]);

        uint256 lastAccountId = accounts[_caip2ChainId].length - 1;
        accounts[_caip2ChainId][accountIndex] = accounts[_caip2ChainId][lastAccountId];
        accounts[_caip2ChainId].pop();
    }
}
```


**Impact:** A chain can exist with zero accounts in scope, violating the check enforced during creation.

**Proof of Concept:** Add the following to `Agreement.t.sol`:

```solidity
 function test_POC_removeAllAccountsFromChain() public {
        AgreementDetails memory detailsBefore = agreement.getDetails();
        assertEq(detailsBefore.chains[0].accounts.length, 1);

        string memory chainId = detailsBefore.chains[0].caip2ChainId;
        string memory accountAddr = detailsBefore.chains[0].accounts[0].accountAddress;

        // Remove the account
        string[] memory toRemove = new string[](1);
        toRemove[0] = accountAddr;

        vm.prank(owner);
        agreement.removeAccounts(chainId, toRemove);

        // Verify chain now has zero accounts
        AgreementDetails memory detailsAfter = agreement.getDetails();
        assertEq(detailsAfter.chains[0].accounts.length, 0);  // @audit chain now has zero accounts

    }
```

**Recommended Mitigation:** Consider adding a check in `Agreement::removeAccounts` to ensure at least one account remains.

**SafeHarbor:**
Fixed in [bf411ed](https://github.com/PatrickAlphaC/safe-harbor/commit/bf411edbace91ad93c1285ac4ac8c391fa338404).

**Cyfrin:** Verified.

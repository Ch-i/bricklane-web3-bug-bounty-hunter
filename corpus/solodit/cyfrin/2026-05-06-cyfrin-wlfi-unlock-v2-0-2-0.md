---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-06-cyfrin-wlfi-unlock-v2-0-2-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-05-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-06-cyfrin-wlfi-unlock-v2-0
title: Duplicated `WLFI` access control check can be extracted into a modifier
vuln_class: []
---

# Duplicated `WLFI` access control check can be extracted into a modifier

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-06-cyfrin-wlfi-unlock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md)_

---

**Description:** Both `WorldLibertyFinancialRegistry` and `WorldLibertyFinancialVester` gate their `wlfi`-prefixed external functions with an identical inline access control check that reverts when the caller is not the `WLFI` contract. The same three-line block is duplicated across four functions in the registry and five functions in the vester.

`WorldLibertyFinancialRegistry`: `wlfiActivateAccount`, `wlfiBurnAllocation`, `wlfiReallocateFrom`, `wlfiSetCategory`.


```solidity
// WorldLibertyFinancialRegistry.sol#L34-L90
function wlfiActivateAccount(address _user) external {
    if (msg.sender != address(WLFI)) {
        revert Unauthorized();
    }
    ...
}

function wlfiBurnAllocation(address _user, uint256 _amount) external {
    if (msg.sender != address(WLFI)) {
        revert Unauthorized();
    }
    ...
}

function wlfiReallocateFrom(address _from, address _to) external {
    if (msg.sender != address(WLFI)) {
        revert Unauthorized();
    }
    ...
}

function wlfiSetCategory(address _user, uint8 _category) external {
    if (msg.sender != address(WLFI)) {
        revert Unauthorized();
    }
    ...
}
```

`WorldLibertyFinancialVester`: `wlfiActivateVest`, `wlfiBurnAllocation`, `wlfiClaimFor`, `wlfiReallocateFrom`, `wlfiSetCategory`.


```solidity
//WorldLibertyFinancialVester.sol#L95-L173
function wlfiActivateVest(address _user, uint8 _category, uint112 _amount) external whenNotPaused {
    if (msg.sender != address(WLFI)) {
        revert Unauthorized();
    }
    ...
}

function wlfiBurnAllocation(address _user, uint256 _amount) external whenNotPaused {
    if (msg.sender != address(WLFI)) {
        revert Unauthorized();
    }
    ...
}

function wlfiClaimFor(address _user) external whenNotPaused returns (uint256) {
    if (msg.sender != address(WLFI)) {
        revert Unauthorized();
    }
    ...
}

function wlfiReallocateFrom(address _from, address _to) external whenNotPaused {
    if (msg.sender != address(WLFI)) {
        revert Unauthorized();
    }
    ...
}

function wlfiSetCategory(address _user, uint8 _category) external whenNotPaused {
    if (msg.sender != address(WLFI)) {
        revert Unauthorized();
    }
    ...
}
```

**Impact:** Code duplication. A future change to the authorization rule requires editing nine call sites across two contracts, which increases the risk of inconsistent updates.

**Recommended Mitigation:** Extract the check into a modifier and apply it to each `wlfi`-prefixed function in both contracts.

```solidity
modifier onlyWLFI() {
    if (msg.sender != address(WLFI)) {
        revert Unauthorized();
    }
    _;
}

// Registry
function wlfiActivateAccount(address _user) external onlyWLFI {
    _activateAccount(_user);
}

function wlfiBurnAllocation(address _user, uint256 _amount) external onlyWLFI {
    ...
}

function wlfiReallocateFrom(address _from, address _to) external onlyWLFI {
    ...
}

function wlfiSetCategory(address _user, uint8 _category) external onlyWLFI {
    ...
}

// Vester
function wlfiActivateVest(address _user, uint8 _category, uint112 _amount) external onlyWLFI whenNotPaused {
    _activateVest(_user, _category, _amount);
}

function wlfiBurnAllocation(address _user, uint256 _amount) external onlyWLFI whenNotPaused {
    ...
}

function wlfiClaimFor(address _user) external onlyWLFI whenNotPaused returns (uint256) {
    return _claim(_user);
}

function wlfiReallocateFrom(address _from, address _to) external onlyWLFI whenNotPaused {
    ...
}

function wlfiSetCategory(address _user, uint8 _category) external onlyWLFI whenNotPaused {
    ...
}
```

**WLFI:** Fixed in commit [1430e24](https://github.com/worldliberty/usd1-protocol/commit/1430e245349795921bebe275f6bd1d835d9f8fa3).

**Cyfrin:** Verified.

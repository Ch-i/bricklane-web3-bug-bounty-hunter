---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: '`Karma.sol` doesn''t initialize signature variables'
vuln_class: []
---

# `Karma.sol` doesn't initialize signature variables

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** Karma.sol only calls following initializers:
```solidity
contract Karma is Initializable, ERC20VotesUpgradeable, UUPSUpgradeable, AccessControlUpgradeable {

    function initialize(address _owner) public initializer {
        ...
        __ERC20_init(NAME, SYMBOL);
        __ERC20Votes_init();
        __UUPSUpgradeable_init();
        __AccessControl_init();

        ...
    }
```

However `ERC20VotesUpgradeable` inherits `ERC20PermitUpgradeable`:
```solidity
abstract contract ERC20VotesUpgradeable is Initializable, IVotesUpgradeable, ERC20PermitUpgradeable {
```
```solidity
    /**
     * @dev Initializes the {EIP712} domain separator using the `name` parameter, and setting `version` to `"1"`.
     *
     * It's a good idea to use the same `name` that is defined as the ERC20 token name.
     */
    function __ERC20Permit_init(string memory name) internal onlyInitializing {
        __EIP712_init_unchained(name, "1");
    }
```

**Impact:** It means `Karma.sol` uses `name = ""` and `version = 0` for EIP712 signature, which makes it incompatible with digital wallets. I.e. function `ERC20VotesUpgradeable::delegateBySig` can't be used.

**Recommended Mitigation:** Initialize ERC20Permit:
```diff
    function initialize(address _owner) public initializer {
        ...
        __ERC20_init(NAME, SYMBOL);
+       __ERC20Permit_init(NAME);
        __ERC20Votes_init();
        __UUPSUpgradeable_init();
        __AccessControl_init();

        ...
    }
```

**StatusL2:** Fixed in [7d447fd](https://github.com/status-im/status-network-monorepo/commit/7d447fd66db824bf210214ef5c06cc4fb2e3dcd8).

**Cyfrin:** Verified.

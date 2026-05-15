---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-4-10
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Remove `decimals` from initial `RemoraToken` mint
vuln_class: []
---

# Remove `decimals` from initial `RemoraToken` mint

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** `RemoraToken` overrides the `decimals` function to return 0 as its tokens are non-fractional:
```solidity
    /**
     * @notice Defines the number of decimal places for the token.
     * RWA tokens are non-fractional and operate in whole units only.
     * @return The number of decimals (always `0`).
     */
    function decimals() public pure override returns (uint8) {
        return 0;
    }
```

So remove the call to `decimals` inside `RemoraToken::initialize` since `10 ** decimals()` will always evaluate to 1:
```diff
    function initialize(
        address tokenOwner,
        address initialAuthority,
        address stablecoin,
        address wallet,
        address _allowList,
        string memory _name,
        string memory _symbol,
        uint256 _initialSupply
    ) public initializer {
        // does this order matter?, open zeppelin upgrades giving errors here
        __ERC20_init(_name, _symbol);
        __ERC20Permit_init(_name);
        __Pausable_init();
        __RemoraBurnable_init();
        __RemoraLockUp_init(0); //start with 0 lock up time
        __RemoraDocuments_init(_name, "1");
        __RemoraHolderManagement_init(
            initialAuthority,
            stablecoin,
            wallet,
            0 //starts at zero, will need to update it later
        );
        __UUPSUpgradeable_init();

        allowlist = _allowList;
        _whitelist[tokenOwner] = true; //whitelist owner to be able to send tokens freely
-       _mint(tokenOwner, _initialSupply * 10 ** decimals());
+       _mint(tokenOwner, _initialSupply);
    }
```

**Remora:** Fixed in commit [462d2de](https://github.com/remora-projects/remora-smart-contracts/commit/462d2def8f09453435e4df433228cfaa565d2e37).

**Cyfrin:** Verified.

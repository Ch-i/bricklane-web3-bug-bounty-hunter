---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-quill-finance-report-1-12
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-quill-finance-report
title: '[L-13] Missing DisableInitializers'
vuln_class: []
---

# [L-13] Missing DisableInitializers

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Quill_Finance_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md)_

---

**Impact**

The following contracts are now upgradeable

They do not `disableInitializers` on the logic

This is a code smell, I have yet to weaponize

And due to how the system works I doubt it will cause many issues


https://github.com/subvisual/quill/blob/d4a5dcc168dfc315eef6a4c9c465a36c86ca0ddc/contracts/src/HintHelpers.sol#L11-L20

```solidity
contract HintHelpers is QuillUUPSUpgradeable, IHintHelpers {
    string public constant NAME = "HintHelpers";

    ICollateralRegistry public collateralRegistry;

    function initialize(address _authority, ICollateralRegistry _collateralRegistry) public initializer {
        __QuillUUPSUpgradeable_init(_authority);
        collateralRegistry = _collateralRegistry;
    }

```

https://github.com/subvisual/quill/blob/d4a5dcc168dfc315eef6a4c9c465a36c86ca0ddc/contracts/src/MultiTroveGetter.sol#L11-L17

```solidity
contract MultiTroveGetter is QuillUUPSUpgradeable, IMultiTroveGetter {
    ICollateralRegistry public collateralRegistry;

    function initialize(address _authority, ICollateralRegistry _collateralRegistry) public initializer {
        __QuillUUPSUpgradeable_init(_authority);
        collateralRegistry = _collateralRegistry;
    }
```

https://github.com/subvisual/quill/blob/d4a5dcc168dfc315eef6a4c9c465a36c86ca0ddc/contracts/src/CollateralRegistry.sol#L42-L55

```solidity

    function initialize(address _authority, IBoldToken _boldToken, ISequencerSentinel _sequencerSentinel)
        public
        initializer
    {
        __QuillUUPSUpgradeable_init(_authority);
        lastFeeOperationTime = block.timestamp;
        boldToken = _boldToken;
        sequencerSentinel = _sequencerSentinel;

        // Initialize the baseRate state variable
        baseRate = INITIAL_BASE_RATE;
        emit BaseRateUpdated(INITIAL_BASE_RATE);
    }
```

https://github.com/subvisual/quill/blob/d4a5dcc168dfc315eef6a4c9c465a36c86ca0ddc/contracts/src/BoldToken.sol#L43-L49

```solidity

    function initialize(address _authority) public initializer {
        __ERC20_init(_NAME, _SYMBOL);
        __ERC20Permit_init(_NAME);
        __QuillUUPSUpgradeable_init(_authority);
    }

```

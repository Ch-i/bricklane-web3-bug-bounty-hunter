---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-3-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Retrieve and enforce token decimal precision
vuln_class: []
---

# Retrieve and enforce token decimal precision

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** Retrieve and enforce token decimal precision using [`IERC20Metadata`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/extensions/IERC20Metadata.sol). For example:

1) `PledgeManager::initialize`
```diff
    constructor(
        address authority,
        address _holderWallet,
        address _propertyToken,
        address _stablecoin,
-       uint16 _stablecoinDecimals,
        uint32 _fundingGoal,
        uint32 _deadline,
        uint32 _withdrawDuration,
        uint32 _pledgeFee,
        uint32 _earlySellPenalty,
        uint32 _pricePerToken
    ) AccessManaged(authority) ReentrancyGuardTransient() {
        holderWallet = _holderWallet;
        propertyToken = _propertyToken;
        stablecoin = _stablecoin;
-       stablecoinDecimals = _stablecoinDecimals;
+       stablecoinDecimals = IERC20Metadata(_stablecoin).decimals();
        fundingGoal = _fundingGoal;
        deadline = _deadline;
        postDeadlineWithdrawPeriod = _withdrawDuration;
        pledgeFee = _pledgeFee;
        earlySellPenalty = _earlySellPenalty;
        pricePerToken = _pricePerToken;
        tokensSold = 0;
    }
```

2) `TokenBank::initialize`
```diff
        stablecoin = _stablecoin; //must be 6 decimal stablecoin
+       require(IERC20Metadata(stablecoin).decimals() == 6, "Wrong decimals");
```

**Remora:** This was resolved by adding the `remoraToNativeDecimals` which always converts from internal Remora precision to external stablecoin precision, so the protocol can now work with different decimal stablecoins.

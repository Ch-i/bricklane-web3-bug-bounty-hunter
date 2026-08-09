---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-3-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Optimize away old value variables when emitting events by emitting events first
vuln_class: []
---

# Optimize away old value variables when emitting events by emitting events first

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** Optimize away old value variables when emitting events by emitting events first, for example in `BTCY::setWithdrawalFee`:
```diff
-       uint256 oldFee = $.withdrawalFee;
+       emit WithdrawalFeeUpdated($.withdrawalFee;, fee);
        $.withdrawalFee = fee;
-       emit WithdrawalFeeUpdated(oldFee, fee);
```

Also affects:
* `BTCY::setFeeRecipient, setMinWithdrawAmount`
* `DepositWithdraw::setTreasury`
* `IBTCY::setBTCYVault, setComplianceAddress`
* `IBTCYHub::setInstantRedemptionFee, setRegularRedemptionFee, setInstantSubscriptionFee, setRegularSubscriptionFee, setMinimumDepositAmount, setMinimumRedemptionAmount, setFeeRecipient, setComplianceAddress, setPricer`
* `Pricer::setPriceFeed`

**Aarc:** Fixed in commit [0ee5f5c](https://github.com/aarc-xyz/btcy-contracts-main/commit/0ee5f5c0903cf1650ce218a2e1bdae87e17f4d12).

**Cyfrin:** Verified.

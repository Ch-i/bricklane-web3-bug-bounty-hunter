---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0-1-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-12-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0
title: Lack of slippage protection in the SecuritizeVault's liquidation function
vuln_class: []
---

# Lack of slippage protection in the SecuritizeVault's liquidation function

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md)_

---

**Description:** The SecuritizeVault's `liquidate()` function converts share tokens to asset tokens using the NAV provider's rate without allowing users to specify a minimum output amount. Since the conversion rate is dynamic and external redemption may be involved, users are exposed to potential value loss from rate changes between transaction submission and execution. This is particularly concerning in volatile market conditions or when there is high latency in transaction processing.

**Impact:** Users may receive fewer assets than expected during liquidation due to rate changes, leading to direct financial losses.

**Recommended Mitigation:**
1. Add a `minOutputAmount` parameter to the liquidate function:
```solidity
function liquidate(uint256 shares, uint256 minOutputAmount) public override(ISecuritizeVault) whenNotPaused {
...
    require(assets >= minOutputAmount, "Insufficient output amount");
...
}
```
2. Consider implementing a time limit parameter to protect against long-pending transactions
3. Add events to track actual output amounts for monitoring purposes

**Securitize:** Fixed in commit [42e651](https://bitbucket.org/securitize_dev/bc-securitize-vault-sc/commits/42e6511931f03b266b3acd4ca220544246efb4ab).

**Cyfrin:** Verified.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-05-cyfrin-farcaster-1-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-11-05T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-05-cyfrin-farcaster.md
tags:
- firm:cyfrin
- report:2023-11-05-cyfrin-farcaster
title: Lack of validations for some admin functions
vuln_class: []
---

# Lack of validations for some admin functions

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-05-cyfrin-farcaster.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-05-cyfrin-farcaster.md)_

---

In `KeyManager.setUsdFee()` and `StorageRegistry.setPrice()`, there are no upper limits.

While the protocol owner is regarded as a trusted party, it's still kind of an inconsistent implementation because there are min/max limits for `fixedEthUsdPrice` in `StorageRegistry.setFixedEthUsdPrice()`.

```solidity
File: audit-farcaster\src\KeyManager.sol
203:     function setUsdFee(uint256 _usdFee) external onlyOwner {
204:         emit SetUsdFee(usdFee, _usdFee);
205:         usdFee = _usdFee;
206:     }

File: audit-farcaster\src\StorageRegistry.sol
716:     function setPrice(uint256 usdPrice) external onlyOwner {
717:         emit SetPrice(usdUnitPrice, usdPrice);
718:         usdUnitPrice = usdPrice;
719:     }
```

**Client:**
After internal discussion, we’ve decided to remove payments from the `KeyGateway` altogether. (See the response to 7.2.1 for more details).

We don't intend to redeploy the StorageRegistry with this deployment, but we will add this validation in the next version of the storage contract.

Commit: [`11e2722`](https://github.com/farcasterxyz/farcaster-contracts-private/commit/11e27223625e4c6b5f929398e015ccda740c1593)

**Cyfrin:** Acknowledged.

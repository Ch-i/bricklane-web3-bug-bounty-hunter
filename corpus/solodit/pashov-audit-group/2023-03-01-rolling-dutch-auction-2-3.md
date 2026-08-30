---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-03-01-rolling-dutch-auction-2-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-03-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-03-01-Rolling%20Dutch%20Auction.md
tags:
- firm:pashov-audit-group
- report:2023-03-01-rolling-dutch-auction
title: '[M-04] Auction won''t work correctly with fee-on-transfer & rebasing tokens'
vuln_class: []
---

# [M-04] Auction won't work correctly with fee-on-transfer & rebasing tokens

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-03-01-Rolling Dutch Auction.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-03-01-Rolling%20Dutch%20Auction.md)_

---

**Impact:**
High, as it can lead to a loss of value

**Likelihood:**
Low, as such tokens are not so common

**Description**

The code in `createAuction` does the following:

```solidity
IERC20(reserveToken).transferFrom(msg.sender, address(this), reserveAmount);
...
...
state.reserves = reserveAmount;
```

so it basically caches the expected transferred amount. This will not work if the `reserveToken` has a fee-on-transfer mechanism, since the actual received amount will be less because of the fee. It is also a problem if the token used had a rebasing mechanism, as this can mean that the contract will hold less balance than what it cached in `state.reserves` for the auction, or it will hold more, which will be stuck in the protocol.

**Recommendations**

You can either explicitly document that you do not support tokens with a fee-on-transfer or rebasing mechanism or you can do the following:

1. For fee-on-transfer tokens, check the balance before and after the transfer and use the difference as the actual amount received.
2. For rebasing tokens, when they go down in value, you should have a method to update the cached `reserves` accordingly, based on the balance held. This is a complex solution.
3. For rebasing tokens, when they go up in value, you should add a method to actually transfer the excess tokens out of the protocol.

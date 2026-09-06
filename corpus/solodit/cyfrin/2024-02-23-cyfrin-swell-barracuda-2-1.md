---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-2-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-02-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
tags:
- firm:cyfrin
- report:2024-02-23-cyfrin-swell-barracuda
title: Use Checks-Effects-Interactions pattern in `swEXIT::createWithdrawRequest`
vuln_class: []
---

# Use Checks-Effects-Interactions pattern in `swEXIT::createWithdrawRequest`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-02-23-cyfrin-swell-barracuda.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md)_

---

**Description:** The current implementation uses [`_safeMint`](https://github.com/SwellNetwork/v3-contracts-lst/blob/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/swEXIT.sol#L209) before modifying state variables:
* `withdrawalRequests[tokenId] `
* `exitingETH`
* `_lastTokenIdCreated`

This allows possible re-entrancy where the receiver and access the non-updated state variables. While during the audit no meaningful permissionless attack vectors related to this issue were found, to follow best security practices it is advisable to move `_safeMint` to the end of the function:

```diff
  function createWithdrawRequest(
    uint256 amount
  ) external override checkWhitelist(msg.sender) {
    if (AccessControlManager.withdrawalsPaused()) {
      revert WithdrawalsPaused();
    }

    if (amount < withdrawRequestMinimum) {
      revert WithdrawRequestTooSmall(amount, withdrawRequestMinimum);
    }

    if (amount > withdrawRequestMaximum) {
      revert WithdrawRequestTooLarge(amount, withdrawRequestMaximum);
    }

    IswETH swETH = AccessControlManager.swETH();
    swETH.transferFrom(msg.sender, address(this), amount);

    // Burn the tokens first to prevent reentrancy and to validate they own the requested amount of swETH
    swETH.burn(amount);

-   uint256 tokenId = _lastTokenIdCreated + 1; // Start off at 1
+   uint256 tokenId = ++_lastTokenIdCreated; // Starts off at 1

-   _safeMint(msg.sender, tokenId);

    uint256 lastTokenIdProcessed = getLastTokenIdProcessed();

    uint256 rateWhenCreated = AccessControlManager.swETH().swETHToETHRate();

    withdrawalRequests[tokenId] = WithdrawRequest({
      amount: amount,
      timestamp: block.timestamp,
      lastTokenIdProcessed: lastTokenIdProcessed,
      rateWhenCreated: rateWhenCreated
    });

    exitingETH += wrap(amount).mul(wrap(rateWhenCreated)).unwrap();
-   _lastTokenIdCreated = tokenId;
+   _safeMint(msg.sender, tokenId);

    emit WithdrawRequestCreated(
      tokenId,
      amount,
      block.timestamp,
      lastTokenIdProcessed,
      rateWhenCreated,
      msg.sender
    );

  }
```

**Swell:** Fixed in commits [d13aa43](https://github.com/SwellNetwork/v3-contracts-lst/commit/d13aa4390bb75c4e491b9cd92b7f7561cbe4ec15), [3f85df3](https://github.com/SwellNetwork/v3-contracts-lst/commit/3f85df3ba0e91b26e4234b15ad94f492fa6d46ec).

**Cyfrin:**
Verified.

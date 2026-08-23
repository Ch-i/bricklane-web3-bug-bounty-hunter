---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-2-9
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`ArmadaRedemption` : Optional ETH redemption can cause users to forfeit their
  pro-rata ETH share'
vuln_class: []
---

# `ArmadaRedemption` : Optional ETH redemption can cause users to forfeit their pro-rata ETH share

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `ArmadaRedemption:redeem` allows a caller to opt out of receiving native ETH by passing `includeETH = false`, while still transferring their ARM into the redemption contract and receiving ERC20 payouts.

As a result, a caller can unintentionally forfeit their pro-rata ETH share. The unclaimed ETH remains in the redemption contract and can be captured by subsequent redeemers.
From an economic perspective, if a caller is able to receive native ETH successfully, then choosing `includeETH = true` is strictly better than choosing `includeETH = false`, because the caller receives more total value in the same redemption flow. In that case, opting out of ETH does not provide a financial benefit to the redeemer and instead leaves part of their pro-rata entitlement behind for others to claim later.

**Impact:** Callers who redeem with `includeETH = false` lose their pro-rata ETH share even though their ARM is still transferred to the redemption contract. The leftover ETH remains available for later redeemers, causing unexpected redistribution of value.

This is primarily an API and UX issue, but it can still produce real economic loss if an integration, frontend, or caller passes `false` by mistake or treats the flag as harmless or the user rushed to redeem as this is designed in-case of a wind-down.

**Recommended Mitigation:** Consider replacing the `includeETH` bool with a required `ethRecipient` parameter:

```solidity
redeem(uint256 armAmount, address[] calldata tokens, address ethRecipient)
```

and enforce:

- `require(ethRecipient != address(0))`
- always attempt ETH payout as part of redemption


As an alternative design/mitigation, explicitly define the pro-rata payout based on the flag:

- `includeETH = true`: the user receives ETH and a correspondingly smaller ERC20/token share
- `includeETH = false`: the user receives no ETH and a correspondingly larger ERC20/token share


**Armada:** Fixed in commit [cf1ae6f](https://github.com/ship-armada/armada-poc/commit/cf1ae6fc1bc4da8e8584f69fcafc883f82ad2fc0).

**Cyfrin:** Verified.

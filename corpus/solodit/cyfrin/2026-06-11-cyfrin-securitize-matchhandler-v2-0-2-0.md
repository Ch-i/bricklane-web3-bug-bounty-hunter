---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-11-cyfrin-securitize-matchhandler-v2-0-2-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-11T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-11-cyfrin-securitize-matchHandler-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-11-cyfrin-securitize-matchhandler-v2-0
title: Redundant `custodialWallet` storage read on the `matchOrder` settlement path
vuln_class: []
---

# Redundant `custodialWallet` storage read on the `matchOrder` settlement path

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-11-cyfrin-securitize-matchHandler-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-11-cyfrin-securitize-matchHandler-v2.0.md)_

---

**Description:** On the success path of `MatchHandler::matchOrder`, the namespaced storage field `custodialWallet` is loaded from storage twice across separate statements - once to address the fee transfer (only when `totalFee > 0`) and again as the final `emit` argument. The optimizer cannot dedupe these because they span statement boundaries (and an intervening external `safeTransferFrom`). The first read occurs only inside the `totalFee > 0` branch, which also warms the slot, so on a settlement that charges a fee the second read is a redundant warm read (roughly 100 gas saved by caching); when `totalFee` is zero only the event read runs and there is no redundancy. The saving therefore applies per fee-charging settlement on this hot path.

```solidity
contracts/ats/MatchHandler.sol
162:            IERC20(stableCoin).safeTransferFrom(buyer.wallet, _getStorage().custodialWallet, totalFee);
165:        emit Match(seller, buyer.wallet, dsToken, stableCoin, dsTokenAmount, stableCoinAmount, sellerFee, buyerFee, _getStorage().custodialWallet);
```

**Recommended Mitigation:** Read the field once near the top of the fee block and reuse the local in both the transfer and the event:

```solidity
address custodial = _getStorage().custodialWallet;
uint256 totalFee = sellerFee + buyerFee;
if (totalFee > 0) {
    IERC20(stableCoin).safeTransferFrom(buyer.wallet, custodial, totalFee);
}
emit Match(seller, buyer.wallet, dsToken, stableCoin, dsTokenAmount, stableCoinAmount, sellerFee, buyerFee, custodial);
```

**Securitize:** Fixed in commit [`ffe8e33`](https://github.com/securitize-io/bc-ats-sc/commit/ffe8e3398899b0e5ceca7fad2a2485302ffb0110)

**Cyfrin:** Verified.

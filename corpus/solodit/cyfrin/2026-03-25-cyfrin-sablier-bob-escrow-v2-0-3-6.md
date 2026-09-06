---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-3-6
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: Dust WETH permanently stuck in `SablierBob` after adapter vault redemptions
vuln_class: []
---

# Dust WETH permanently stuck in `SablierBob` after adapter vault redemptions

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** In `SablierLidoAdapter::calculateAmountToTransferWithYield` (`SablierLidoAdapter.sol:178`), each user's WETH share is computed with truncating division:

```solidity
uint128 userWethShare = (userWstETH * totalWeth / totalWstETH).toUint128();
```

Each truncation loses up to 1 wei. After all users of an adapter vault redeem, the sum of all individual `userWethShare` values is slightly less than `totalWeth`. The remainder stays in `SablierBob` as WETH with no sweep or recovery function.

For example, with 100 users in a vault, up to 99 wei of WETH could be permanently stuck after all redemptions complete.

**Impact:** The per-vault dust amount is negligible (at most `numUsers - 1` wei of WETH per vault). However, it accumulates across all adapter vaults over the protocol's lifetime and there is no mechanism to recover these funds. The impact is economic dust, not a security risk.

**Recommended Mitigation:** Add an admin-callable sweep function to recover residual WETH from fully-redeemed adapter vaults, or allow the last redeemer to receive the remaining balance instead of their truncated share.

**Sablier:** Acknowledged.

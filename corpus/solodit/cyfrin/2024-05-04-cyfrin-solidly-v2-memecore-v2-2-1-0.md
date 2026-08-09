---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-04-cyfrin-solidly-v2-memecore-v2-2-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-05-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md
tags:
- firm:cyfrin
- report:2024-05-04-cyfrin-solidly-v2-memecore-v2-2
title: Accounts blocked by the token cannot claim their fees
vuln_class: []
---

# Accounts blocked by the token cannot claim their fees

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md)_

---

**Description:** In `SolidlyV2`, liquidity providers accrue fees from trades made in the pool. These fees are bound to the account holding the liquidity position at the time of trading as the fees are synced on transfers.

When the liquidity provider wants to claim their fees they call `SolidlyV2Pair::claimFees`:
```solidity
if (feeState.feeOwed0 > 1) {
    amount0 = feeState.feeOwed0 - 1;
    _safeTransfer(token0, msg.sender, uint256(amount0));
    feesClaimedLP0 += amount0;
    feesClaimedTotal0 += amount0;
    feeState.feeOwed0 = 1;
}
```
Here the tokens are transferred to `msg.sender`.

The issue is that some tokens, such as `USDC`, have block lists where some accounts are blocked from receiving or doing transfers. Were this to happen to `msg.sender`, they would never be able to claim their fees, and these funds would be locked in the pool indefinitely.

**Impact:** If an account is blocked by, for example, `USDC,` the user will not be able to claim their fees.

**Recommended Mitigation:** Add a parameter `address to` to `SolidlyV2Pair::claimFees` so that the fees can be transferred to a different account.

**Solidly Labs:** Acknowledged.

**Cyfrin:** Acknowledged.

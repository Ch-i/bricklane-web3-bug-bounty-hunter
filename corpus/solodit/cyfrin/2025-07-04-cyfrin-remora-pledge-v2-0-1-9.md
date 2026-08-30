---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-1-9
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Payout distributions to Remora token holders are diluted by initial token owner
  mint
vuln_class: []
---

# Payout distributions to Remora token holders are diluted by initial token owner mint

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** `RemoraToken::initialize` takes a parameter `_initialSupply` and mints this to `tokenOwner`:
```solidity
_mint(tokenOwner, _initialSupply * 10 ** decimals());
```

`DividendManager::distributePayout` records the payout amount together with the current total supply:
```solidity
$._payouts[$._currentPayoutIndex++] = PayoutInfo({
    amount: payoutAmount,
    totalSupply: SafeCast.toUint128(totalSupply())
});
```

`DividendManager::payoutBalance` calculates user payout amount dividing by the recorded total supply:
```solidity
payoutAmount +=
    (curEntry.tokenBalance * pInfo.amount) /
    pInfo.totalSupply;
```

**Impact:** Payout distributions for Remora token holders are diluted by the initial token owner mint. If the token owner is minted a significant percentage of the supply, normal users will have their rewards significantly diluted.

**Recommended Mitigation:** Exclude the token owner's tokens from the payout distribution by subtracting them from the total supply. The token owner could get around this though by transferring their tokens to other addresses the control.

Another way is to have a variable in `RemoraToken` which only the admin can set that records the amount of tokens the owner holds, and this gets subtracted from the total supply for purposes of payout distribution. The owner would need to update this variable so there is still trust required in the owner.

Alternatively the finding can be acknowledged as long as the protocol is aware that users will have their rewards diluted by the owner's holdings.

**Remora:** The plan is to send all of the initial token mint to the `TokenBank`; the intended `tokenOwner` is actually the token bank. These tokens then go on sale for the investors so the protocol admin won't hold any tokens themselves; the tokens will either be in the token bank awaiting sale or with the investors who bought them.

Unsold tokens held by `TokenBank` are owned by the protocol; we will use the forwarding mechanism to claim our share of the payout distributions for unsold tokens still held by the token bank.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-2-7
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: '`PaymentSettler::claimAllPayouts` doesn''t validate input `tokens` addresses
  are legitimate contracts before calling `adminClaimPayout` on them'
vuln_class: []
---

# `PaymentSettler::claimAllPayouts` doesn't validate input `tokens` addresses are legitimate contracts before calling `adminClaimPayout` on them

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** In `PaymentSettler::initiateBurning` and `distributePayment`, before calling any functions on the input `token` address this check occurs to ensure it is a legitimate address:
```solidity
if (!tokenData[token].active) revert InvalidTokenAddress();
```

But in `PaymentSettler::claimAllPayouts` this check does not occur:
```solidity
function claimAllPayouts(address[] calldata tokens) external nonReentrant {
    address investor = msg.sender;
    uint256 totalPayout = 0;
    for (uint i = 0; i < tokens.length; ++i) {
        TokenData storage curToken = tokenData[tokens[i]];
        uint256 amount = IRemoraToken(tokens[i]).adminClaimPayout(
            investor,
            true
        );
```

**Impact:** An attacker can deploy their own contract which implements the `adminClaimPayout` function interface but this function can contain arbitrary code; execution flow is transferred to the attacker's contract. We have not found a way to further abuse this but it isn't a good practice to allow an attacker to hijack execution flow into their own custom contracts.

**Recommended Mitigation:** Verify that the input `tokens` are valid `RemoraToken` contracts prior to calling any functions on them.

**Remora:** Fixed in commit [4ba903e](https://github.com/remora-projects/remora-smart-contracts/commit/4ba903e52438e9570940c11ae8c39acf07256b6a).

**Cyfrin:** Verified.

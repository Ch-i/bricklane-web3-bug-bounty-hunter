---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-0-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Attacker can make pledge on behalf of users if those users have approved `PledgeManager`
  to spend their tokens
vuln_class: []
---

# Attacker can make pledge on behalf of users if those users have approved `PledgeManager` to spend their tokens

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** `PledgeManager` requires users to approve it to spend their tokens in order to make pledges. Users can do this by either:
1) using `IERC20Permit::permit` which enforces a nonce for the signer, deadline and domain separator
2) manually by calling `IERC20::approve`

If users use the manual method 2) and leave an open token approval, an attacker can call `PledgeManager::pledge` to make a pledge on their behalf since this function never enforces that `msg.sender == data.signer`.

**Impact:** Attacker can make pledges on behalf of innocent users which spends those users' tokens. It is common for users to have max approvals for protocols they use often, even though they don't intend to spend all their tokens with that protocol.

**Recommended Mitigation:** In `PledgeManager::pledge`, when not using `IERC20Permit::permit` enforce that `msg.sender == data.signer`:
```diff
        if (data.usePermit) {
            IERC20Permit(stablecoin).permit(
                signer,
                address(this),
                finalStablecoinAmount,
                block.timestamp + 300,
                data.permitV,
                data.permitR,
                data.permitS
            );
        }
+       else if(msg.sender != signer) revert MsgSenderNotSigner();
```

Alternatively always use `msg.sender` similar to how `PledgeManager::refundTokens` works.

**Remora:** Fixed in commit [e3bda7c](https://github.com/remora-projects/remora-smart-contracts/commit/e3bda7c78321febb0e2f37b29912ba24c9e04343) by always using `msg.sender` and also removed the permit method.

**Cyfrin:** Verified.

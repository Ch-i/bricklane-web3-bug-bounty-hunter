---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-1-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: '`ERC4626` vaults must override `maxWithdraw, maxDeposit, maxMint, maxRedeem`
  to return zero when paused or for user-specific limits such as being denied access'
vuln_class: []
---

# `ERC4626` vaults must override `maxWithdraw, maxDeposit, maxMint, maxRedeem` to return zero when paused or for user-specific limits such as being denied access

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** [EIP-4626](https://eips.ethereum.org/EIPS/eip-4626) states on `maxDeposit`:
> MUST factor in both global and user-specific limits, like if deposits are entirely disabled (even temporarily) it MUST return 0.

Similar statements in the EIP-4626 standard can be found related to `maxWithdraw, maxMint, maxRedeem`. If pausing or other limits are not accounted for by these functions this violates EIP-4626 which can break integrating protocols expecting standards-compliant behavior.

In the context of `BTCY`, these functions should return zero when:
* contract is paused
* `isTransferDenylisted(user) == true` (see check in `_update`)
* for `maxWithdraw, maxRedeem` when `isAllowlisted(user) == false` and when the withdrawn amount would be smaller than `$.minWithdrawAmount` (see checks in `_withdraw`)

**Aarc:** Fixed in commit [ac4f562](https://github.com/aarc-xyz/btcy-contracts-main/pull/11/changes/ac4f562ed8133a2d058d4aec2bed3efbea7f3dd6), [2e39ebf](https://github.com/aarc-xyz/btcy-contracts-main/pull/11/changes/2e39ebf64259fdedd7dbd06c3c028fcd479798b7).

**Cyfrin:** Verified.

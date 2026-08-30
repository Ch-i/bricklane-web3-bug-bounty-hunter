---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-1-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Fees should round up in favor of the protocol
vuln_class: []
---

# Fees should round up in favor of the protocol

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** Fees should round up in favor of the protocol:
* `BTCY::_calculateWithdrawalFee`
* `IBTCYHub::_getRedemptionFees, _getSubscriptionFees`

**Recommended Mitigation:** Use OZ [mulDiv](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/math/Math.sol#L282-L284) with explicit rounding.

It has become best practice to always:
* use explicit rounding directions
* comment each with the logical reason for why the rounding direction is correct in that place

This forces developers to carefully consider each rounding direction which is important since incorrect rounding directions have frequently been part of mainnet hack exploit chains.

**Aarc:** Fixed in commit [b603dfa](https://github.com/aarc-xyz/btcy-contracts-main/pull/11/changes/b603dfab6d6123c63fc321cd6b7d00e03ed4431d).

**Cyfrin:** Verified.

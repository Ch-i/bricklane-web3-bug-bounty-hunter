---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-23-cyfrin-strata-shares-cooldown-v2-0-2-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-01-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-23-cyfrin-strata-shares-cooldown-v2-0
title: Parameter `at` in `SharesCooldown::finalize` is functionally redundant
vuln_class: []
---

# Parameter `at` in `SharesCooldown::finalize` is functionally redundant

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md)_

---

**Description:** The `finalize` functions expose an `at` parameter that suggests the ability to finalize claims “as of” a specific timestamp. In practice this parameter provides no real control or flexibility. The only validation applied is `at <= block.timestamp`.

```solidity
function extractClaimableInner(address vault, address user, uint256 at) internal returns (uint256 claimable) {
        if (at > block.timestamp) {
            revert InvalidTime();
        }
        ...

        uint256 len = requests.length;
        for (uint256 i; i < len; ) {
            ..
            if (isCooldownActive && req.unlockAt > at)
        }
        ...
    }
```

As a result, passing any `at` value in the past yields the same behavior as passing `block.timestamp`, and there is no way to use `at` to selectively finalize a subset of requests or to simulate historical finalization.

**Recommended Mitigation:** Remove `finalize` with `at` functions

**Strata:** Acknowledged. This parameter allows users to finalize only a subset of completed requests, rather than all eligible redemption requests at once.

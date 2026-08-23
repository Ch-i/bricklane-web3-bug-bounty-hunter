---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-02-cyfrin-stakelink-vesting-v2-0-1-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-08-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-02-cyfrin-stakelink-vesting-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-02-cyfrin-stakelink-vesting-v2-0
title: Consider disabling the owner to renounce ownership
vuln_class: []
---

# Consider disabling the owner to renounce ownership

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-02-cyfrin-stakelink-vesting-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-02-cyfrin-stakelink-vesting-v2.0.md)_

---

**Description:** `Ownable`’s default `renounceOwnership()` allows the owner to relinquish control entirely by setting owner to `address(0)`, which can be called unintentionally. To avoid permanent loss of privileged functions, consider overriding `renounceOwnership` to disable or restrict it. For example:

```solidity
function renounceOwnership() public view override onlyOwner {
    revert("Renouncing ownership is disabled");
}
```

This ensures ownership can only change via deliberate `transferOwnership` (or `Ownable2Step`), preventing accidental or irreversible renouncement.


**Stake.Link:** Acknowledged.

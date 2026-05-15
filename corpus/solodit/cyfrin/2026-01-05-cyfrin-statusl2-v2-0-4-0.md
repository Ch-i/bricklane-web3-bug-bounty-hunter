---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-4-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: Incorrect Natspec in `RLN::setSlashRevealWindowTime`
vuln_class: []
---

# Incorrect Natspec in `RLN::setSlashRevealWindowTime`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** Comment mentions max value of `365 days`, however actual code bounds by `1 days`:
```solidity
    /// @dev Sets the slash reveal window time.
    /// @param _slashRevealWindowTime: new reveal window time in seconds.
@>  /// @notice The window time must be at least 1 second and no more than 365 days.
    ///         A non-zero value is required to ensure the queuing mechanism functions correctly.
    ///         An excessively large value could lock commitments indefinitely.
    function setSlashRevealWindowTime(uint256 _slashRevealWindowTime) external onlyRole(DEFAULT_ADMIN_ROLE) {
@>      if (_slashRevealWindowTime == 0 || _slashRevealWindowTime > 1 days) {
            revert RLN__InvalidSlashRevealWindowTime(_slashRevealWindowTime);
        }

        slashRevealWindowTime = _slashRevealWindowTime;
    }
```

**Recommended Mitigation:** Update Natspec

**StatusL2:** Fixed in [1f8414d](https://github.com/status-im/status-network-monorepo/commit/1f8414daa55e8955de7baef428e5ea2c14104327).

**Cyfrin:** Verified.

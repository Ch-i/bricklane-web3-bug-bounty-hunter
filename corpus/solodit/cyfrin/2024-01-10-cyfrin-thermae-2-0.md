---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-10-cyfrin-thermae-2-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-01-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-10-cyfrin-thermae.md
tags:
- firm:cyfrin
- report:2024-01-10-cyfrin-thermae
title: Use low level `call()` to prevent gas griefing attacks when returned data not
  required
vuln_class: []
---

# Use low level `call()` to prevent gas griefing attacks when returned data not required

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-10-cyfrin-thermae.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-10-cyfrin-thermae.md)_

---

**Description:** Using `call()` when the returned data is not required unnecessarily exposes to gas griefing attacks from huge returned data payload. For example:
```solidity
(bool sentToUser, ) = recipient.call{ value: finalUserAmount }("");
require(sentToUser, "Failed to send Ether");
```

Is the same as writing:
```solidity
(bool sentToUser, bytes memory data) = recipient.call{ value: finalUserAmount }("");
require(sentToUser, "Failed to send Ether");
```

In both cases the returned data will be copied into memory exposing the contract to gas griefing attacks, even though the returned data is not used at all.

**Impact:** Contract unnecessarily exposed to gas griefing attacks.

**Recommended Mitigation:** Use a low-level call when the returned data is not required, eg:
```solidity
bool sent;
assembly {
    sent := call(gas(), recipient, finalUserAmount, 0, 0, 0, 0)
}
if (!sent) revert Unauthorized();
```

Consider using [ExcessivelySafeCall](https://github.com/nomad-xyz/ExcessivelySafeCall).

**Wormhole:**
Fixed in commit 5f3926b.

**Cyfrin:** Verified.

\clearpage

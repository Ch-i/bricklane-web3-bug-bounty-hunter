---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-20-cyfrin-mode-earnm-2-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-11-20T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md
tags:
- firm:cyfrin
- report:2023-11-20-cyfrin-mode-earnm
title: Use low level `call()` to prevent gas griefing attacks when returned data not
  required
vuln_class: []
---

# Use low level `call()` to prevent gas griefing attacks when returned data not required

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-20-cyfrin-mode-earnm.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md)_

---

**Description:** Using `call()` when the returned data is not required unnecessarily exposes to gas griefing attacks from huge returned data payload. For [example](https://github.com/Earnft/smart-contracts/blob/43d3a8305dd6c7325339ed35d188fe82070ee5c9/contracts/MysteryBox.sol#L197-L198):
```solidity
(bool sent, ) = address(operatorAddress).call{value: msg.value}("");
if (!sent) revert Unauthorized();
```
Is the same as writing:
```solidity
(bool sent, bytes memory data) = address(operatorAddress).call{value: msg.value}("");
if (!sent) revert Unauthorized();
```
In both cases the returned data will have to be copied into memory exposing the contract to gas griefing attacks, even though the returned data is not required at all.

**Impact:** Contracts unnecessarily expose themselves to gas griefing attacks.

**Recommended Mitigation:** Use a low-level call when the returned data is not required, eg:

```solidity
bool sent;
assembly {
    sent := call(gas(), receiver, amount, 0, 0, 0, 0)
}
if (!sent) revert Unauthorized();
```
Consider using [ExcessivelySafeCall](https://github.com/nomad-xyz/ExcessivelySafeCall).

**Mode:**
Fixed in commit [85b2012](https://github.com/Earnft/smart-contracts/commit/85b20121604b5d162bb14c2c96731b8345ca1cb3).

**Cyfrin:** Verified.

\clearpage

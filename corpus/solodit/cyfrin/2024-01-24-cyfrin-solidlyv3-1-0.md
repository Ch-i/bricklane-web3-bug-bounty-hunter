---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-24-cyfrin-solidlyv3-1-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md
tags:
- firm:cyfrin
- report:2024-01-24-cyfrin-solidlyv3
title: Use low level `call()` to prevent gas griefing attacks when returned data not
  required
vuln_class: []
---

# Use low level `call()` to prevent gas griefing attacks when returned data not required

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-24-cyfrin-solidlyV3.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md)_

---

**Description:** Using `call()` when the returned data is not required unnecessarily exposes to gas griefing attacks from huge returned data payload. For [example](https://github.com/SolidlyV3/v3-rewards/blob/6dfb435392ffa64652c8f88c98698756ca80cf28/contracts/RewardsDistributor.sol#L563-L564):

```solidity
(bool sent, ) = _to.call{value: _amount}("");
require(sent);
```

Is the same as writing:

```solidity
(bool sent, bytes memory data) = _to.call{value: _amount}("");
require(sent);
```

In both cases the returned data will be copied into memory exposing the contract to gas griefing attacks, even though the returned data is not used at all.

**Impact:** Contract unnecessarily exposed to gas griefing attacks.

**Recommended Mitigation:** Use a low-level call when the returned data is not required, eg:

```solidity
bool sent;
assembly {
    sent := call(gas(), _to, _amount, 0, 0, 0, 0)
}
if (!sent) revert FailedToSendEther();
```

**Solidly:**
Fixed in commit [be54da1](https://github.com/SolidlyV3/v3-rewards/commit/be54da1fea0f1f6f3e4c6ee20464b962cbe2077f).

**Cyfrin:**
Verified.

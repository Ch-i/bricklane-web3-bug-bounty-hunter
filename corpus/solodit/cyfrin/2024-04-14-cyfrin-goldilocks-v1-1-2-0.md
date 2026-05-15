---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-2-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-04-14T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
tags:
- firm:cyfrin
- report:2024-04-14-cyfrin-goldilocks-v1-1
title: '`Goldivault.changeProtocolParameters()` shouldn''t update `endTime`.'
vuln_class: []
---

# `Goldivault.changeProtocolParameters()` shouldn't update `endTime`.

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-14-cyfrin-goldilocks-v1.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md)_

---

**Description:** `Goldivault.changeProtocolParameters()` updates `endTime` only without changing `startTime`.

```solidity
  function changeProtocolParameters(
    uint256 _earlyWithdrawalFee,
    uint256 _yieldFee,
    uint256 _delay,
    uint256 _duration
  ) external {
    if(msg.sender != timelock) revert NotTimelock();
    earlyWithdrawalFee = _earlyWithdrawalFee;
    yieldFee = _yieldFee;
    delay = _delay;
    duration = _duration;
    endTime = block.timestamp + _duration;
  }
```

It's more appropriate not to update `endTime` as this function is just to change parameters.

**Client:** Fixed in [PR #11](https://github.com/0xgeeb/goldilocks-core/pull/11)

**Cyfrin:** Verified.

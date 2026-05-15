---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-3-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: '`totalMaxMP` incorrectly accounts for individual `maxMP`'
vuln_class: []
---

# `totalMaxMP` incorrectly accounts for individual `maxMP`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** Each stake has a limit of MP to accrue, accrual must stop after 4 years. For each stake it calculates `maxMP` and simply stops accrual after that value, and it is correct:
```solidity
    function _calculateAccrual(
        uint256 _balance,
        uint256 _currentTotalMP,
        uint256 _currentMaxMP,
        uint256 _lastAccrualTime,
        uint256 _processTime
    )
        internal
        pure
        returns (uint256 _deltaMpTotal)
    {
        uint256 dt = _processTime - _lastAccrualTime;
@>      if (_currentTotalMP < _currentMaxMP) {
@>          _deltaMpTotal = Math.min(_accrueMP(_balance, dt), _currentMaxMP - _currentTotalMP);
        }
    }
```

However such approach is incorrect for `totalMaxMP` value:
```solidity
    function _totalMP() internal view returns (uint256) {
        if (totalMaxMP == 0) {
            return totalMPAccrued;
        }

        uint256 currentTime = block.timestamp;
        uint256 timeDiff = currentTime - lastMPUpdatedTime;
        if (timeDiff == 0) {
            return totalMPAccrued;
        }

@>      uint256 accruedMP = _accrueMP(totalStaked, timeDiff);
@>      if (totalMPAccrued + accruedMP > totalMaxMP) {
@>          accruedMP = totalMaxMP - totalMPAccrued;
        }

        uint256 newTotalMPAccrued = totalMPAccrued + accruedMP;

        return newTotalMPAccrued;
    }
```

That's because total value doesn't know how much from `totalStaked` has already approached the limit, so it uses full amount for accrual.
Suppose following scenario:
1) There are 2 stakes of 1000 tokens (suppose both with 4 years lock), i.e. `totalMaxMP = 1000 * 9 * 2 = 18000`. The only difference is that one of them has accrued max MP because lives for 4 years.
2) It means that actually MP grows only based on 1000 staked.
3) But `StakeManager::_totalMP` will accrue MP using `totalStaked = 2000`. And this line won't save, because capacity is more than enough  `9000 + 5000 > 18000 ---> false` :
```solidity
        if (totalMPAccrued + accruedMP > totalMaxMP) {
            accruedMP = totalMaxMP - totalMPAccrued;
        }
```

**Impact:** `StakeManager::totalMPAccrued` and `StakeManager::totalMP` inflate real values.

**Recommended Mitigation:** Fix is not trivial.

**StatusL2:** Fixed in [56a7b64](https://github.com/status-im/status-network-monorepo/commit/56a7b64a782150b2a87563621212b076e35f84f5).

**Cyfrin:** Verified.

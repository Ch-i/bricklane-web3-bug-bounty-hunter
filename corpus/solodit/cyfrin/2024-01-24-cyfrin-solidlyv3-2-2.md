---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-24-cyfrin-solidlyv3-2-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md
tags:
- firm:cyfrin
- report:2024-01-24-cyfrin-solidlyv3
title: '`require` and `revert` statements should have descriptive reason strings'
vuln_class: []
---

# `require` and `revert` statements should have descriptive reason strings

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-24-cyfrin-solidlyV3.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md)_

---

**Description:** `require` and `revert` statements should have descriptive reason strings:

```solidity
File: SolidlyV3Factory.sol

46:         require(tokenA != tokenB);

48:         require(token0 != address(0));

50:         require(tickSpacing != 0);

51:         require(getPool[token0][token1][tickSpacing] == address(0));

61:         require(msg.sender == owner);

68:         require(msg.sender == owner);

75:         require(msg.sender == owner);

88:         require(msg.sender == owner);

89:         require(fee <= 100000);

94:         require(tickSpacing > 0 && tickSpacing < 16384);

95:         require(feeAmountTickSpacing[fee] == 0);

```

```solidity
File: SolidlyV3Pool.sol

116:         require(success && data.length >= 32);

127:         require(success && data.length >= 32);

302:         require(amount > 0);

327:         require(amount > 0);

947:         require(fee <= 100000);

```

```solidity
File: libraries/FullMath.sol

34:             require(denominator > 0);

43:         require(denominator > prod1);

120:             require(result < type(uint256).max);

```

```solidity
File: RewardsDistributor.sol

564:        require(sent);

595:        require(success && data.length >= 32);

```

**Solidly:**
Acknowledged.

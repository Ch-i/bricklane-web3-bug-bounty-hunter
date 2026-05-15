---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-25
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[L-26] `ERC20.Permit` can be front-runned and should be try/catched'
vuln_class: []
---

# [L-26] `ERC20.Permit` can be front-runned and should be try/catched

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

Permit can be broadcasted by anyone and will revert if using the incorrect nonce

Due to this you should use try/catch it

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/BorrowerOperations.sol#L225-L245

```solidity
  function openTroveWithPermit(
    TokenAmount[] memory _colls,
    bytes[] memory _priceUpdateData,
    uint deadline,
    uint8[] memory v,
    bytes32[] memory r,
    bytes32[] memory s
  ) external payable {
    for (uint i = 0; i < _colls.length; i++)
      IERC20Permit(_colls[i].tokenAddress).permit( /// @audit Should use Permit
        msg.sender,
        address(this),
        _colls[i].amount,
        deadline,
        v[i],
        r[i],
        s[i]
      );

    openTrove(_colls, _priceUpdateData);
  }
```

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/SwapOperations.sol#L317-L318

```solidity
    IERC20Permit(tokenA).permit(msg.sender, address(this), amountADesired, deadline, v[0], r[0], s[0]);
    IERC20Permit(tokenB).permit(msg.sender, address(this), amountBDesired, deadline, v[1], r[1], s[1]);
```

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/SwapOperations.sol#L511

```solidity
IERC20Permit(path[0]).permit(msg.sender, address(this), amountIn, deadline, v, r, s);
```

See this article for more info:
https://www.trust-security.xyz/post/permission-denied

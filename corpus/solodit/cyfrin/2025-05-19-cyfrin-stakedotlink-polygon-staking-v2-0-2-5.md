---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0-2-5
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-05-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0
title: No slippage protection when interacting with `ValidatorShares`
vuln_class: []
---

# No slippage protection when interacting with `ValidatorShares`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md)_

---

**Description:** In the `PolygonVault.sol` contract, the `buyVoucherPOL` and `sellVoucherPOL` functions do not set a slippage limit.

```solidity
// PolygonVault
    function deposit(uint256 _amount) external onlyVaultController {
        token.safeTransferFrom(msg.sender, address(this), _amount);

        // @audit-issue - no slippage limit.
@>        validatorPool.buyVoucherPOL(_amount, 0);

        uint256 balance = token.balanceOf(address(this));
        if (balance != 0) token.safeTransfer(msg.sender, balance);
    }

   function unbond(uint256 _amount) external onlyVaultController {
         // @audit-issue no slippage limit
@>         validatorPool.sellVoucherPOL(_amount, type(uint256).max);

        uint256 balance = token.balanceOf(address(this));
        if (balance != 0) token.safeTransfer(msg.sender, balance);
    }
```

Currently, there is no active slashing in `ValidatorShares`, therefore loss of funds cannot occur.

**Recommended Mitigation:** Keep monitoring Polygon PoS governance for slashing updates; if implemented, upgrade the contract to support slashing accordingly.


**[Project]:**
Acknowledged. Will implement slippage protection if slashing is introduced.

**Cyfrin:** Acknowledged.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0-2-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-05-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0
title: Missing zero address checks
vuln_class: []
---

# Missing zero address checks

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md)_

---

**Description:** Critical address in the controller, strategy and vault contracts have missing zero address checks, both at the time of initialization and later, at the time of updates.

`PolygonStrategy.sol`
```solidity
    function setValidatorMEVRewardsPool(address _validatorMEVRewardsPool) external onlyOwner {
        validatorMEVRewardsPool = IRewardsPool(_validatorMEVRewardsPool); //@audit missing zero address check
    }

   function setVaultImplementation(address _vaultImplementation) external onlyOwner { //@audit missing zero address check
        vaultImplementation = _vaultImplementation;
        emit SetVaultImplementation(_vaultImplementation);
    }
```

`PolygonFundFlowController.sol`
```solidity
   function setDepositController(address _depositController) external onlyOwner {
        depositController = _depositController; // @audit missing zero address check
    }
```

**Recommended Mitigation:** Consider introducing zero address checks at all places highlighted above.

**Stake.Link:** Resolved in [PR 151](https://github.com/stakedotlink/contracts/pull/151/commits/9889b7b628050dbc791f028aeb8b9ff8b21cd93a)

**Cyfrin:** Resolved.

---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-quill-finance-report-3-5
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-quill-finance-report
title: '[I-05] Key Security Invariants'
vuln_class: []
---

# [I-05] Key Security Invariants

_Section severity (from Solodit section header): Informational_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Quill_Finance_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md)_

---

---

**Whenever I open a trove, I get the debt assigned to me, with at most 1e9 in error**

**I can never open a trove and be liable for zero debt**

**Once a Batch is rebased, no new troves can be opened in it, nor added to it, nor any debt can be increased**
The only succesful function must be `removeTroveFromBatch`

---

**Shutdown only ever reverts becasue of this error**
No other reason

https://github.com/subvisual/quill/blob/d4a5dcc168dfc315eef6a4c9c465a36c86ca0ddc/contracts/src/BorrowerOperations.sol#L1222-L1223

```solidity
        if (TCR >= SCR()) revert TCRNotBelowSCR();

```

**Shutdown only ever reverts becasue of this error**
No other reason

https://github.com/subvisual/quill/blob/d4a5dcc168dfc315eef6a4c9c465a36c86ca0ddc/contracts/src/BorrowerOperations.sol#L1222-L1223

```solidity
        if (TCR >= SCR()) revert TCRNotBelowSCR();

```


**_activePool.getCollBalance() - _collRemainder**
Never revert


**Never Revert**
https://github.com/GalloDaSballo/quill-review/blob/8d6e4c8ed0759cea1ff0376db9fd55db864cd7e8/contracts/src/TroveManager.sol#L1096-L1103

```solidity
    function _updateSystemSnapshots_excludeCollRemainder(IActivePool _activePool, uint256 _collRemainder) internal {
        totalStakesSnapshot = totalStakes;

        uint256 activeColl = _activePool.getCollBalance();
        uint256 liquidatedColl = defaultPool.getCollBalance();
        totalCollateralSnapshot = activeColl - _collRemainder + liquidatedColl;
    }

```



**Stake math**

My stake accurately represents my % deposits of all collateral (ignoring precision loss due to redistribution and division)

https://github.com/GalloDaSballo/quill-review/blob/8d6e4c8ed0759cea1ff0376db9fd55db864cd7e8/contracts/src/TroveManager.sol#L1037-L1053

```solidity

    function _computeNewStake(uint256 _coll) internal view returns (uint256) {
        uint256 stake;
        if (totalCollateralSnapshot == 0) {
            stake = _coll;
        } else {
            /*
            * The following assert() holds true because:
            * - The system always contains >= 1 trove
            * - When we close or liquidate a trove, we redistribute the redistribution gains, so if all troves were closed/liquidated,
            * rewards would’ve been emptied and totalCollateralSnapshot would be zero too.
            */
            // assert(totalStakesSnapshot > 0);
            stake = _coll * totalStakesSnapshot / totalCollateralSnapshot;
        }
        return stake;
    }
```

**Never reverts with Overflow**

https://github.com/subvisual/quill/blob/23e53123a16b12614d25bfb715e17dd41bcebbdd/contracts/src/TroveManager.sol#L299-L307

```solidity

    function _liquidate(
        IDefaultPool _defaultPool,
        uint256 _troveId,
        uint256 _boldInStabPool,
        uint256 _price,
        LatestTroveData memory trove,
        LiquidationValues memory singleLiquidation
    ) internal {
```

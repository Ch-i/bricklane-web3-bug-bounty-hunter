---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-quill-finance-report-1-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-quill-finance-report
title: '[L-03] Sequencer Sentinel Config can be updated to follow first principles'
vuln_class: []
---

# [L-03] Sequencer Sentinel Config can be updated to follow first principles

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Quill_Finance_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md)_

---

**Impact**

The sequencer sentinel has 2 types of checks:
- `_requireSequencerUpAndOverGracePeriod` - Safer check, ensures that prices are updated
- `_requireSequencerUp` - Less safe check, prices may not be updated

A check that is less safe could be used for operations that reduce risk to the system, such as repaying, closing and adding collateral

A check that is safer should be used for everything else


**Increase Risk - Should wait for Grace Period**

The following should be changed to use `_requireSequencerUpAndOverGracePeriod`

https://github.com/subvisual/quill/blob/d4a5dcc168dfc315eef6a4c9c465a36c86ca0ddc/contracts/src/BorrowerOperations.sol#L520-L528

```solidity
    function adjustTroveInterestRate(
        uint256 _troveId,
        uint256 _newAnnualInterestRate,
        uint256 _upperHint,
        uint256 _lowerHint,
        uint256 _maxUpfrontFee
    ) external {
        _requireSequencerUp();
        _requireIsNotShutDown();
```

https://github.com/subvisual/quill/blob/d4a5dcc168dfc315eef6a4c9c465a36c86ca0ddc/contracts/src/BorrowerOperations.sol#L929-L939

```solidity

    function setBatchManagerAnnualInterestRate(
        uint128 _newAnnualInterestRate,
        uint256 _upperHint,
        uint256 _lowerHint,
        uint256 _maxUpfrontFee
    ) external {
        _requireSequencerUp();
        _requireIsNotShutDown();
        _requireValidInterestBatchManager(msg.sender);
        _requireInterestRateInBatchManagerRange(msg.sender, _newAnnualInterestRate);
```

https://github.com/subvisual/quill/blob/d4a5dcc168dfc315eef6a4c9c465a36c86ca0ddc/contracts/src/BorrowerOperations.sol#L1066-L1074

```solidity
    function removeFromBatch(
        uint256 _troveId,
        uint256 _newAnnualInterestRate,
        uint256 _upperHint,
        uint256 _lowerHint,
        uint256 _maxUpfrontFee
    ) public override {
        _requireSequencerUp();
        _requireIsNotShutDown();
```

**NOTE: MORE**

https://github.com/subvisual/quill/blob/23e53123a16b12614d25bfb715e17dd41bcebbdd/contracts/src/BorrowerOperations.sol#L996-L1005

```solidity
    function setInterestBatchManager(
        uint256 _troveId,
        address _newBatchManager,
        uint256 _upperHint,
        uint256 _lowerHint,
        uint256 _maxUpfrontFee
    ) public override {
        _requireSequencerUp();
        _requireIsNotShutDown();
        LocalVariables_setInterestBatchManager memory vars;
```

---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-kleidi-report-0-11
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-kleidi-report
title: '[L-12] Once a `RecoverySpell` is deployed, all spells on all chains may be
  deployed'
vuln_class: []
---

# [L-12] Once a `RecoverySpell` is deployed, all spells on all chains may be deployed

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Kleidi_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md)_

---

**Impact**

RecoverySpells are meant to be used in a time of emergency

For various reasons a recovery may need to be performed exclusively on one chain

However, calling `createRecoverySpell` will leak key details about the RecoverySpell

https://github.com/solidity-labs-io/kleidi/blob/1a06ac16bc99d0b4081281329d03064c3737f5e4/src/RecoverySpellFactory.sol#L44-L51

```solidity
    function createRecoverySpell(
        bytes32 salt,
        address[] memory owners,
        address safe,
        uint256 threshold,
        uint256 recoveryThreshold,
        uint256 delay
    ) external returns (RecoverySpell recovery) {
```

More specifically it will inform everyone about the parameters that would result in the RecoverySpell being deployed on every other chain

In the scenario in which a recovery was meant to be performed only on Chain A, for all other chains, anyone could deploy the RecoverySpell causing them to have a reduced delay for all those chains

**Mitigation**

In your documentation you should clarify that if recovery happens on one chain, it should probably happen on all chains

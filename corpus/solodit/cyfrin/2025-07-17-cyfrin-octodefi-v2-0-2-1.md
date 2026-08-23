---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-2-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-07-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-17-cyfrin-octodefi-v2-0
title: '`automationsToIndex` storage is not correctly reset when deleting automations'
vuln_class: []
---

# `automationsToIndex` storage is not correctly reset when deleting automations

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-17-cyfrin-octodefi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md)_

---

**Description:** When deleting an automation, the logic pops the final element from the `_usedInAutomations` array but fails to correctly reset the `automationsToIndex` mapping storage. Regardless of whether the if statement executes, `automationsToIndex[automationSID]` should be reset to zero whenever there is a deletion:

```solidity
    function _deleteAutomation(address wallet, uint32 id) internal {
        bytes32 automationSID = getStorageId(wallet, id);
        Automation memory _automation = automations[automationSID];

        uint32[] storage _usedInAutomations = strategiesUsed[getStorageId(wallet, _automation.strategyId)];

@>      uint32 _actualAutomationIndex = automationsToIndex[automationSID];
        uint256 _lastAutomationIndex = _usedInAutomations.length - 1;
        if (_actualAutomationIndex != _lastAutomationIndex) {
            uint32 _lastAutomation = _usedInAutomations[_lastAutomationIndex];
            _usedInAutomations[_actualAutomationIndex] = _lastAutomation;
@>          automationsToIndex[getStorageId(wallet, _lastAutomation)] = _actualAutomationIndex;
        }
        _usedInAutomations.pop();

        _changeAutomationInCondition(
            wallet, _automation.condition.conditionAddress, _automation.condition.id, id, false
        );

        delete automations[automationSID];

        emit AutomationDeleted(wallet, id);
    }
```

**Impact:** Impact is limited as it seems the mapping will simply be overwritten if the automation is ever added again at the same id, and given `_usedInAutomations` is correctly popped it does not seem that the entry will be erroneously referenced.

**Recommended Mitigation:** Reset the mapping value for the given automation storage id when deleting the corresponding automation.

**OctoDeFi:** Fixed in PR [#17](https://github.com/octodefi/strategy-builder-plugin/pull/17).

**Cyfrin:** Verified. The relevant `automationsToIndex` mapping key is now cleared alongside `automations`.

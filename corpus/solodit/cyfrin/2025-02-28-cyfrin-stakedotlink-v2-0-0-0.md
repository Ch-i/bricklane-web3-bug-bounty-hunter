---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-02-28-cyfrin-stakedotlink-v2-0-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-02-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-02-28-cyfrin-stakedotlink-v2.0.md
tags:
- firm:cyfrin
- report:2025-02-28-cyfrin-stakedotlink-v2-0
title: Lack of events emitted on state changes
vuln_class: []
---

# Lack of events emitted on state changes

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-02-28-cyfrin-stakedotlink-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-02-28-cyfrin-stakedotlink-v2.0.md)_

---

**Description:** The following functions should ideally emit an event to enhance transparency and traceability:


[`Vault::setDelegateRegistry`](https://github.com/stakedotlink/audit-2025-02-linkpool/blob/046c65a9c771315816bc59533183f52661af8e5e/contracts/linkStaking/base/Vault.sol#L180-L186) and [`VaultControllerStrategy::setDelegateRegistry`](https://github.com/stakedotlink/audit-2025-02-linkpool/blob/046c65a9c771315816bc59533183f52661af8e5e/contracts/linkStaking/base/VaultControllerStrategy.sol#L708-L714):

```diff
  function setDelegateRegistry(address _delegateRegistry) external onlyOwner {
      delegateRegistry = _delegateRegistry;
+     emit SetDelegateRegistry(_delegateRegistry);
  }
```

[`FundFlowController::setNonLINKRewardReceiver`](https://github.com/stakedotlink/audit-2025-02-linkpool/blob/046c65a9c771315816bc59533183f52661af8e5e/contracts/linkStaking/FundFlowController.sol#L325-L331):

```diff
  function setNonLINKRewardReceiver(address _nonLINKRewardReceiver) external onlyOwner {
      nonLINKRewardReceiver = _nonLINKRewardReceiver;
+     emit SetNonLINKRewardReceiver(_nonLINKRewardReceiver);
  }
```

Additionally, an event could be emitted when rewards are withdrawn in [`FundFlowController::withdrawTokenRewards`](https://github.com/stakedotlink/audit-2025-02-linkpool/blob/046c65a9c771315816bc59533183f52661af8e5e/contracts/linkStaking/FundFlowController.sol#L307-L323):
```diff
  function withdrawTokenRewards(address[] calldata _vaults, address[] calldata _tokens) external {
      // ...
+     emit WithdrawTokenRewards(msg.sender, _vaults, _tokens);
  }
```

Consider adding events to these functions to provide a clear on-chain record of when and by whom these actions were executed. This improves transparency and makes it easier to track changes.

**Stake.Link:** Acknowledged.

**Cyfrin:** Acknowledged.

\clearpage

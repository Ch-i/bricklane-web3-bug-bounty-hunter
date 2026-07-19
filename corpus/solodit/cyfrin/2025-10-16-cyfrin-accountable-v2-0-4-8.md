---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-accountable-v2-0-4-8
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-accountable-v2-0
title: State changes without events
vuln_class: []
---

# State changes without events

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-accountable-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md)_

---

There are state variable changes in this function but no event is emitted. Consider emitting an event to enable offchain indexers to track the changes.

- [Line: 47](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/modules/GlobalRegistry.sol#L47)

	```solidity
	    function setSecurityAdmin(address securityAdmin_) external onlyOwner {
	```

- [Line: 53](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/modules/GlobalRegistry.sol#L53)

	```solidity
	    function setOperationsAdmin(address operationsAdmin_) external onlyOwner {
	```

- [Line: 59](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/modules/GlobalRegistry.sol#L59)

	```solidity
	    function setTreasury(address treasury_) external onlyOwner {
	```

- [Line: 65](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/modules/GlobalRegistry.sol#L65)

	```solidity
	    function setVaultFactory(address vaultFactory_) external onlyOwner {
	```

- [Line: 71](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/modules/GlobalRegistry.sol#L71)

	```solidity
	    function setRewardsFactory(address rewardsFactory_) external onlyOwner {
	```

**Accountable:** Fixed in commit [`13600f4`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/13600f460f9796f16d151d19dc4a1d5c35c1475d)

**Cyfrin:** Verified.

\clearpage

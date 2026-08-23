---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-01-cyfrin-metamask-totalbalanceenforcer-v2-0-2-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-09-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-metamask-TotalBalanceEnforcer-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-01-cyfrin-metamask-totalbalanceenforcer-v2-0
title: Misleading documentation in afterAllHook() natspec
vuln_class: []
---

# Misleading documentation in afterAllHook() natspec

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-01-cyfrin-metamask-TotalBalanceEnforcer-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-metamask-TotalBalanceEnforcer-v2.0.md)_

---

**Description:** In `ERC20TotalBalanceChangeEnforcer :: afterAllHook()` , the natspec says "This function validates that the recipient's token balance has changed by at least the total expected amount", which is incorrect.

In case of the net effect being expected decrease, the actual balance change allowed is limited by a max decrease, in which case balance does not change by "at least an expected amount".

Similarly, natspec of `afterAllHook()` in these enforcers is unclear :
- ERC1155TotalBalanceChangeEnforcer
- ERC721TotalBalanceChangeEnforcer
- NativeTokenTotalBalanceChangeEnforcer

For example, in `ERC1155TotalBalanceChangeEnforcer`, it says "This function enforces that the recipient's ERC1155 token balance has changed by the expected amount". But this could be interpreted as "Balance should always change by the expected amount", while in case of a net expected decrease, a change thats lower than that of "expected maxDecrease" is also allowed.


**Impact:** Incorrect natspec can mislead developers into misunderstanding the design of these enforcers.

**Recommended Mitigation:** The natspec at all these places shall be changed to "This function validates that the recipient's token balance has changed within expected limits".

**Metamask:** Resolved in [PR 144](https://github.com/MetaMask/delegation-framework/pull/144/commits/7e680b27e29aaa1caaacd33286d1346376cab3c3).

**Cyfrin:** Verified.

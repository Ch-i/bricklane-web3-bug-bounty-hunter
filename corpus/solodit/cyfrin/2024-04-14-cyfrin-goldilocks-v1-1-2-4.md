---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-2-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-04-14T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
tags:
- firm:cyfrin
- report:2024-04-14-cyfrin-goldilocks-v1-1
title: Wrong comment
vuln_class: []
---

# Wrong comment

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-14-cyfrin-goldilocks-v1.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md)_

---

**Description:**
```solidity
File: Timelock.sol
49:   /// @notice Delay for queueing a transaction in blocks //@audit seconds, not blocks
60:   /// @param _delay Delay the timelock will use, in blocks //@audit seconds, not blocks
103:   /// @param eta Duration of time until transaction can be executed, in blocks //@audit seconds, not blocks
123:   /// @param eta Duration of time until transaction can be executed, in blocks //@audit seconds, not blocks
154:   /// @param eta Duration of time until transaction can be executed, in blocks //@audit seconds, not blocks

File: Goldilend.sol
496:   /// @notice Calculates claimable Porridge per GiBGT //@audit claimable reward token
608:   /// @dev Claims existing vault rewards and updates poolSize //@audit this function doesn't update poolSize
```
**Client:** Fixed in [PR #16](https://github.com/0xgeeb/goldilocks-core/pull/16)

**Cyfrin:** Verified.

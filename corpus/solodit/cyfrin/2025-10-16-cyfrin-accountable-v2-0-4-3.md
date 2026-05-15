---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-accountable-v2-0-4-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-accountable-v2-0
title: Violations of ERC7540 specs
vuln_class: []
---

# Violations of ERC7540 specs

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-accountable-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md)_

---

**Description:** Several deviations from the ERC7540 specs have been noticed for `AccountableAsyncRedeemVault`

1. According to [ERC-7540](https://eips.ethereum.org/EIPS/eip-7540) specification:

> Redeem Request approval of shares for a msg.sender NOT equal to owner may come either from ERC-20 approval over the shares of owner or if the owner has approved the msg.sender as an operator.

The current implementation in `requestRedeem()` only supports operator approval (from owner to caller). The contract does not implement the ERC-20 allowance path for share approval, limiting the request redeem functionality to only operator-approved addresses.

2. As per the EIP,

> All requests with the same requestID MUST transition from Pending to Claimable state at the same time, and receive the same exchange rate

This means the request should always gets processed in full. Right now, the vault implementation allows partial redemptions and that too at different share prices (if processingMode == CurrentPrice).


**Impact:** Non-compliance with ERC7540.

**Recommended Mitigation:** Consider documenting if the vault is intended to be completely compliant with the EIP, and if so, consider changing the implementation accordingly.

**Accountable:** We acknowledge this as it's not our intention to be 100% compliant, we will document this.

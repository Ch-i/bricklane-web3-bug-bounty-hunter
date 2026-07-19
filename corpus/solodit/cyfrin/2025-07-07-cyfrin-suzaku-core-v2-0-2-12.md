---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-2-12
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-07-07T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-07-cyfrin-suzaku-core-v2-0
title: Overpayment vulnerability in `registerL1`
vuln_class: []
---

# Overpayment vulnerability in `registerL1`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-07-cyfrin-suzaku-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md)_

---

**Description:** The `registerL1` function in the `L1Registry` contract does not handle excess Ether sent by users. If the `registerFee` is set to a nonzero value and a user sends more Ether than required, the contract keeps the entire amount instead of refunding the excess. If the `registerFee` is set to zero and a user sends Ether, that Ether becomes trapped in the contract with no way for the user to recover it, as there is no refund logic or withdrawal path for arbitrary senders.

**Impact:** Users can unintentionally lose funds by sending more Ether than required for registration. In the case where `registerFee` is zero, any Ether sent is permanently locked in the contract, as only the fee collector can withdraw accumulated fees, and only if they were tracked as unclaimed fees. This can lead to user frustration and loss of funds due to simple mistakes or misunderstandings about the required payment.

**Recommended Mitigation:** Implement logic in the `registerL1` function to refund any excess Ether sent above the required `registerFee`. For example, after transferring the required fee to the collector, track any remaining balance for the sender. Additionally, if `registerFee` is zero, revert the transaction if any Ether is sent, preventing accidental loss of funds.

**Suzaku:**
Fixed in commit [1c4cfe6](https://github.com/suzaku-network/suzaku-core/pull/155/commits/1c4cfe6a785287263b83f6c877678ba779abb3fb).

**Cyfrin:** Verified.

\clearpage

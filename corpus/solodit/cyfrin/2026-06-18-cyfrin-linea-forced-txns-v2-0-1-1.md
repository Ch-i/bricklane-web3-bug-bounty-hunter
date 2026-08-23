---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-18-cyfrin-linea-forced-txns-v2-0-1-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-18-cyfrin-linea-forced-txns-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-18-cyfrin-linea-forced-txns-v2-0
title: Missing code to track and withdraw forced transaction fees
vuln_class: []
---

# Missing code to track and withdraw forced transaction fees

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-18-cyfrin-linea-forced-txns-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-18-cyfrin-linea-forced-txns-v2.0.md)_

---

**Description:** When users call `ForcedTransactionGateway::submitForcedTransaction` they send the required fee as `msg.value`. This function passes the fee (`msg.value`) to `LineaRollupBase::storeForcedTransaction` but `LineaRollupBase` doesn't:
* track the total amount of received forced transaction fees
* contain a function to withdraw the fees

Consider at least tracking the total amount of received forced transaction fees and potentially adding a function to withdraw them.

**Linea:** Acknowledged; adding a withdraw function by Linea for any value (tracked or untracked) introduces questions and undue suspicion. Creating a function for this would cause more community concern than needed, so this is not really an option.

Any fees paid are ok to be "donated" to the ecosystem and provide extra cushioning or staking value. We don't expect this to be uses regularly and the amounts are mostly negligible.

The amounts can be calculated easily by using the `ForcedTransactionAdded` type events and getting the transaction value send as this is a 1:1 for the fees paid - no more, no less.

If there was ever a withdraw of this specific amount, it would go through a security council upgrade with a fixed call with the amount that can be publicly traceable.

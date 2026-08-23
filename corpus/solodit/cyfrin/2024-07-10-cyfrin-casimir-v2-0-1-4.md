---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-1-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-07-10T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-10-cyfrin-casimir-v2-0
title: Centralization risks with a lot of power vested in the `Reporter` role
vuln_class: []
---

# Centralization risks with a lot of power vested in the `Reporter` role

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-10-cyfrin-casimir-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md)_

---

**Description:** In the current design, the `Reporter`, a protocol-controlled address, is responsible for executing a number of mission-critical operations. Only `Reporter` operations include starting & finalizing a report, selecting & replacing operators, syncing/activating/withdrawing and depositing validators, verifying & claiming rewards from EigenLayer, etc. Also noteworthy is the fact that the timing and sequence of these operations are crucial for the proper functioning of the Casimir protocol.

**Impact:** With so many operations controlled by a single address, a significant part of which are initiated off-chain, the protocol is exposed to all the risks associated with centralization. Some of the known risks include:

- Compromised/lost private keys that control the `Reporter` address
- Rogue admin
- Network downtime
- Human/Automation errors associated with the execution of multiple operations

**Recommended Mitigation:** While we understand that the protocol in the launch phase wants to retain control over mission-critical parameters, we strongly recommend implementing the following even at the launch phase:

- Continuous monitoring of off-chain processes
- Reporter automation via a multi-sig

In the long term, the protocol should consider a clear path towards decentralization.

**Casimir:**
Acknowledged. We plan to implement the expected EigenLayer checkpoint upgrade that significantly reduces the intervention of the reporter while syncing validator balances.

**Cyfrin:** Acknowledged.

\clearpage

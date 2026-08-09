---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-23-mozaic-archimedes-0-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-05-23T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md
tags:
- firm:trust-security
- report:2023-05-23-mozaic-archimedes
title: TRST-H-1 An attacker can drain Mozaic Vaults by manipulating the LP price
vuln_class: []
---

# TRST-H-1 An attacker can drain Mozaic Vaults by manipulating the LP price

_Section severity (from Solodit section header): High_  
_Audit firm: Trust Security_  
_Source report: [2023-05-23-Mozaic Archimedes.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md)_

---

**Description:**
The controller is tasked with synchronizing LP token price across all chains. It implements a 
lifecycle. An admin initiates the snapshot phase, where Controller requests all Vaults to report 
the total stable ($) value and LP token supply. Once all reports are in, admin calls the settle 
function which dispatches the aggregated value and supply to all vaults. At this point, vaults 
process all deposits and withdrawals requested up to the last snapshot, using the universal 
value/supply ratio. 
The described pipeline falls victim to an economic attack, stemming from the fact that LP 
tokens are LayerZero OFT tokens which can be bridged. An attacker can use this property to 
bypass counting of their LP tokens across all chains. When the controller would receive a
report with correct stable value and artificially low LP supply, it would cause queued LP 
withdrawals to receive incorrectly high dollar value.
To make vaults miscalculate, attacker can wait for Controller to initiate snapshotting. At that 
moment, they can start bridging a large amount of tokens. They may specify custom LayerZero 
adapter params to pay a miniscule gas fee, which will guarantee that the bridge-in transaction 
will fail due to out-of-gas. At this point, they simply wait until all chains have been
snapshotted, and then finish bridging-in with a valid gas amount. Finally, Controller will order 
vaults to settle, at which point the attacker converts their LP tokens at an artificially high price.
Another clever way to exploit this flaw is to count LP tokens multiple times, by quickly 
transporting them to additional chains just before those chains are snapshotted. This way, the 
LP tokens would be diluted and the attacker can get a disproportionate amount of LP tokens 
for their stables.

**Recommended Mitigation:**
The easy but limiting solution is to reduce complexity and disable LP token bridging across 
networks. The other option is to increase complexity and track incoming/outgoing bridge 
requests in the LP token contract. When snapshotting, cross reference the requested 
snapshot time with the bridging history. 

**Team response:**
Fixed.

**Mitigation Review:**
Mozaic's response is to disable LP token bridging altogether. As this is a configuration-level 
fix, users are encouraged to confirm the tokens are not linked via bridges at runtime.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-20-cyfrin-mode-earnm-1-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-11-20T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md
tags:
- firm:cyfrin
- report:2023-11-20-cyfrin-mode-earnm
title: Minting can be indefinitely stuck due to request timeout of external adapters
  when using Chainlink Any API
vuln_class: []
---

# Minting can be indefinitely stuck due to request timeout of external adapters when using Chainlink Any API

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-20-cyfrin-mode-earnm.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md)_

---

**Description:** Mode has integrated Chainlink Any API to interact with external adapters, verifying user codes and wallet addresses to determine the number of boxes to mint. The system uses a `direct-request` job type, triggering actions based on the `ChainlinkRequested` event emission. However, there's a notable issue: if the initial GET request times out, such requests may remain pending indefinitely. Current design does not have a provision to cancel pending requests and create new ones.

**Impact:** If the external adapter doesn't respond promptly, users are unable to submit another minting request because their code is deleted after the initial request. This could result in users losing their codes and not receiving their mystery box rewards.

**Recommended Mitigation:** Consider implementing a function that code recipients can invoke in the event of a request timeout. This function should internally call `ChainlinkClient:cancelChainlinkRequest` and include a callback to the `MysteryBox` contract to initiate a new request using the same data as the original. Essentially, this means reusing the code/user address and the previously generated random number for the new request.

**Mode:**
Acknowledged.


\clearpage

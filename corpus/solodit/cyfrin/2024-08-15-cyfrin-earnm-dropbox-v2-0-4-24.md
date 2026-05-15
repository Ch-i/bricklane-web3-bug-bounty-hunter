---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-4-24
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Delete fulfilled vrf request from `vrfRequestIdToRequester` in `VRFHandler::fulfillRandomWords`
vuln_class: []
---

# Delete fulfilled vrf request from `vrfRequestIdToRequester` in `VRFHandler::fulfillRandomWords`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** Delete fulfilled vrf request from `vrfRequestIdToRequester` in `VRFHandler::fulfillRandomWords`:
```diff
  function fulfillRandomWords(uint256 _requestId, uint256[] calldata _randomWords) internal override {
    // Check if the request has already been fulfilled
    if (vrfFulfilledRequests[_requestId]) revert InvalidVrfState();

    // Cache the contract that requested the random numbers based on the request ID
    address contractRequestor = vrfRequestIdToRequester[_requestId];

    // Revert if the contract that requested the random numbers is not found
    if (contractRequestor == address(0)) revert InvalidVrfState();

+   // delete the active requestId -> requestor record
+   delete vrfRequestIdToRequester[_requestId];

    // Mark the request as fulfilled
    vrfFulfilledRequests[_requestId] = true;

    // Decrement the counter of outstanding requests
    activeRequests--;

    // Call the contract that requested the random numbers with the random numbers
    IVRFHandlerReceiver(contractRequestor).fulfillRandomWords(_requestId, _randomWords);
  }
```

**Mode:**
Fixed in commit [08d7ce4](https://github.com/Earnft/dropbox-smart-contracts/commit/08d7ce40f24e958b51528233f57b99f4333c7501).

**Cyfrin:** Verified.

\clearpage

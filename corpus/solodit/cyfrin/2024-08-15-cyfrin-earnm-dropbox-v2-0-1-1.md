---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-1-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Use upgradeable or replaceable `VRFHandler` contracts when interacting with
  Chainlink VRF
vuln_class: []
---

# Use upgradeable or replaceable `VRFHandler` contracts when interacting with Chainlink VRF

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** Cyfrin has been made aware by our private audit clients that Chainlink intends on bricking VRF 2.0 at the end of November 2024 such that _"VRF 2.0 will stop working"_ even for existing subscriptions.

**Impact:** All immutable contracts dependent on VRF 2.0 will be bricked when Chainlink bricks VRF 2.0. The same will apply in the future to immutable contracts depending on VRF 2.5 when/if Chainlink does the same to it.

**Recommended Mitigation:** Immutable contracts should be insulated from directly interacting with Chainlink VRF. One way to achieve this is to create a separate `VRFHandler` contract that acts as a bridge between immutable contracts and Chainlink VRF; this contract should:
* be either a replaceable immutable contract using [VRFConsumerBaseV2Plus](https://github.com/smartcontractkit/chainlink/blob/develop/contracts/src/v0.8/vrf/dev/VRFConsumerBaseV2Plus.sol) such that a new `VRFHandler` can be deployed, or an upgradeable contract using [VRFConsumerBaseV2Upgradeable](https://github.com/smartcontractkit/chainlink/blob/develop/contracts/src/v0.8/vrf/dev/VRFConsumerBaseV2Upgradeable.sol)
* allow the contract owner to set the address of the immutable contract (and vice versa in the immutable contract to set the address of the `VRF Handler`)
* provide an API to the immutable contract that will not need to change
* handle all the Chainlink VRF API calls and callbacks, passing randomness back to the immutable contract as required

**Mode:**
Fixed in commit [dc3412f](https://github.com/Earnft/dropbox-smart-contracts/commit/dc3412fda8bf988bac579d215c1b7f8f58b973a1) by implementing a replaceable immutable `VRFHandler` contract to act as a bridge between `DropBox` and Chainlink VRF.

**Cyfrin:** Verified.

\clearpage

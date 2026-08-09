---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-4-23
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Remove redundant check from `VRFHandler::constructor`
vuln_class: []
---

# Remove redundant check from `VRFHandler::constructor`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** Remove redundant check from `VRFHandler::constructor`:
```diff
  constructor(
    address vrfCoordinator,
    bytes32 keyHash,
    uint256 subscriptionId
  )
    /**
     * ConfirmedOwner(msg.sender) is defined in @chainlink/contracts/src/v0.8/vrf/dev/VRFConsumerBaseV2Plus.sol:113:40
     * with "msg.sender".
     */
    VRFConsumerBaseV2Plus(vrfCoordinator)
  {
    if (keyHash == bytes32(0)) revert InvalidVrfKeyHash();
    if (subscriptionId == 0) revert InvalidVrfSubscriptionId();
-   if (vrfCoordinator == address(0)) revert InvalidVrfCoordinator();

    vrfKeyHash = keyHash;
    vrfSubscriptionId = subscriptionId;
  }
```

This check is redundant as `VRFHandler` inherits from `VRFConsumerBaseV2Plus` which already [performs](https://github.com/smartcontractkit/chainlink/blob/develop/contracts/src/v0.8/vrf/dev/VRFConsumerBaseV2Plus.sol#L114-L115) this check in its own constructor.

**Mode:**
Fixed in commit [cc45c9a](https://github.com/Earnft/dropbox-smart-contracts/commit/cc45c9a80980118107ede5001ee9ac5c7a5b6040).

**Cyfrin:** Verified.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-3-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Use named imports instead of importing the entire namespace
vuln_class: []
---

# Use named imports instead of importing the entire namespace

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** Use named imports as they offer a number of [advantages](https://ethereum.stackexchange.com/a/117173) compared to importing the entire namespace.

File: `DropBox.sol`
```solidity
// DropBoxFractalProtocol
import {DropBoxFractalProtocol} from "./DropBoxFractalProtocol.sol";

// VRF Handler Interface
import {IVRFHandler} from "./IVRFHandler.sol";
import {IVRFHandlerReceiver} from "./IVRFHandlerReceiver.sol";

// LimitBreak implementations of ERC721C and Programmable Royalties
import {OwnableBasic, OwnablePermissions} from "@limitbreak/creator-token-standards/src/access/OwnableBasic.sol";
import {ERC721C, ERC721OpenZeppelin} from "@limitbreak/creator-token-standards/src/erc721c/ERC721C.sol";
import {BasicRoyalties, ERC2981} from "@limitbreak/creator-token-standards/src/programmable-royalties/BasicRoyalties.sol";

// OpenZeppelin
import {ReentrancyGuard} from "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {Strings} from "@openzeppelin/contracts/utils/Strings.sol";
```

File: `VRFHandler.sol`
```solidity
// VRF Handler Interface
import {IVRFHandler} from "./IVRFHandler.sol";
import {IVRFHandlerReceiver} from "./IVRFHandlerReceiver.sol";

// Chainlink
import {VRFConsumerBaseV2Plus} from "@chainlink/contracts/src/v0.8/vrf/dev/VRFConsumerBaseV2Plus.sol";
import {IVRFCoordinatorV2Plus} from "@chainlink/contracts/src/v0.8/vrf/dev/interfaces/IVRFCoordinatorV2Plus.sol";
import {VRFV2PlusClient} from "@chainlink/contracts/src/v0.8/vrf/dev/libraries/VRFV2PlusClient.sol";
```

**Mode:**
Fixed in commit [9afe010](https://github.com/Earnft/dropbox-smart-contracts/commit/9afe0109afb01cd30f00393bf00f817c3a39a205).

**Cyfrin:** Verified.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-3-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-07-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1
title: Misleading comments and documentation inconsistencies in on-ramp contracts
vuln_class: []
---

# Misleading comments and documentation inconsistencies in on-ramp contracts

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md)_

---

**Description:** Multiple contracts in the on-ramp system contain misleading comments, incorrect documentation, and interface inconsistencies that misrepresent the actual functionality.

- The ```ISecuritizeOnRamp``` interface documents a ```Buy``` event that is never emitted anywhere in the codebase, and references a non-existent ```swapFor``` function in the ```toggleInvestorSubscription``` documentation.

- The ```ISecuritizeOnRamp``` interface incorrectly declares ```nonceByInvestor``` and ```calculateDsTokenAmount``` as state-changing functions when they are actually view functions in the implementation.

- ```MintingAssetProvider``` uses ```@title IAssetProvider``` instead of its actual contract name, creating confusion about which contract is being documented.

- ```IAssetProvider::securitizeOnRamp``` function documentation contains a typo referring to "on ramo contract" instead of "on ramp contract".

- `MpbsFeeManager::setRedemptionFee` function documentation mentions the fee percentage is in basis points while it is supposed to be MBPS.

**Impact:** These misleading comments can cause developers to incorrectly integrate with the contracts by expecting functionality that doesn't exist.

**Securitize:** Fixed in commit [2b6c3a](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/2b6c3a8efdc23b4e2fc5fed273987830fbeaee18).

**Cyfrin:** Verified.

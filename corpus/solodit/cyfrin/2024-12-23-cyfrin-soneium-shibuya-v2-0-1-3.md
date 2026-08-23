---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-23-cyfrin-soneium-shibuya-v2-0-1-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-12-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-23-cyfrin-soneium-shibuya-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-23-cyfrin-soneium-shibuya-v2-0
title: Incomplete ERC20 interface support
vuln_class: []
---

# Incomplete ERC20 interface support

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-23-cyfrin-soneium-shibuya-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-23-cyfrin-soneium-shibuya-v2.0.md)_

---

**Description:** The `supportsInterface()` function doesn't declare support for `IERC20` interface ID despite implementing ERC20 functionality.
This could cause issues with interface detection in some integration scenarios.

**Recommended Mitigation:** Add support for `type(IERC20).interfaceId` in the `supportsInterface` function.

**Startale:** Fixed in commit [cb5b05](https://github.com/StartaleLabs/ccip-contracts-registration/commit/cb5b05c4f09b449aa46b5e6290456f9f94cdb09f).

**Cyfrin:** Verified.

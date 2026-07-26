---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-02-cyfrin-evo-soulboundtoken-v2-0-2-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-06-02T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md
tags:
- firm:cyfrin
- report:2025-06-02-cyfrin-evo-soulboundtoken-v2-0
title: Prefer `calldata` to `memory` for external read-only inputs
vuln_class: []
---

# Prefer `calldata` to `memory` for external read-only inputs

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md)_

---

**Description:** Prefer `calldata` to `memory` for external read-only inputs:
```diff
-   function mintWithTerms(bytes memory signature) external payable returns (uint256 tokenId) {
+   function mintWithTerms(bytes calldata signature) external payable returns (uint256 tokenId) {

-   function _verifySignature(bytes memory signature) internal view returns (bool) {
+   function _verifySignature(bytes calldata signature) internal view returns (bool) {
```

Gas results:
```diff
{
-  "mintWithTerms": "137638"
+  "mintWithTerms": "137299"
}
```

**Evo:**
Fixed in commit [b4fcadb](https://github.com/contractlevel/sbt/commit/b4fcadbd9c5684cc4e3b1ee3c39f72c406aaf658).

**Cyfrin:** Verified.

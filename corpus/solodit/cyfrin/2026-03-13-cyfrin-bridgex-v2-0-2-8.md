---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-2-8
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-bridgex-v2-0
title: Removed releaser sign still count
vuln_class: []
---

# Removed releaser sign still count

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** When `Bridge::removeReleaser` is called, the contract only sets `isReleaser[_releaser] = false` and removes the address from the releasers array. It does not clear or adjust any existing signature state. So for every release that the removed releaser had already signed, `signatures[txHash][_releaser]` stays true and `signatureCount[txHash]` is unchanged. Those past signatures remain valid and still count toward the threshold when other releasers call `Bridge::signRelease`.

**Recommended Mitigation:** When removing a releaser, do not change past signatures/signatureCount but document that removed releasers’ existing signatures still count and that `requiredSignatures` / releaser set should be managed with that in mind, or introduce a way to invalidate in-progress releases that include the removed releaser’s signature

**BridgeX:**
Acknowledged; generally releasers will only be rotated when there are emergencies and the bridge is paused. Addressing this would add a degree of complexity for little gain so we will not implement at this time.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-24-cyfrin-linea-4-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-05-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md
tags:
- firm:cyfrin
- report:2024-05-24-cyfrin-linea
title: Remove redundant modifiers from `TokenBridge::bridgeTokenWithPermit`
vuln_class: []
---

# Remove redundant modifiers from `TokenBridge::bridgeTokenWithPermit`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-24-cyfrin-linea.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md)_

---

**Description:** Since `TokenBridge::bridgeTokenWithPermit` calls `bridgeToken`, it doesn't need to repeat the same modifiers that `bridgeToken` contains; this just incurs additional gas costs.

The only benefit to the redundant modifiers is they make the transaction revert faster but in the majority of normal cases where non-zero inputs are passed these additional redundant modifiers simply increase the gas cost of every successful bridging transaction for regular users.

Remove the `nonZeroAddress`, `nonZeroAmount` and `whenNotPaused` modifiers from `bridgeTokenWithPermit` since they are already enforced by `bridgeToken`.

**Linea:**
Fixed in commit [35c7807](https://github.com/Consensys/zkevm-monorepo/commit/35c7807756ccac2756be7da472f5e6ce0fd9b16a#diff-e5dcf44cdbba69f5a1f8fc58700577ce57caac0c15a5d5fb63e0620aeced62d4L217-R212) merged in [PR3249](https://github.com/Consensys/zkevm-monorepo/pull/3249/files#diff-e5dcf44cdbba69f5a1f8fc58700577ce57caac0c15a5d5fb63e0620aeced62d4L217-R217).

**Cyfrin:** Verified.

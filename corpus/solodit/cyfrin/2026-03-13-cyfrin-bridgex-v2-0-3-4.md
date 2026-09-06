---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-3-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-bridgex-v2-0
title: Cache storage to avoid identical storage reads
vuln_class: []
---

# Cache storage to avoid identical storage reads

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** In Solidity reading from storage is expensive; cache storage to avoid identical storage reads when the value can't change:
* `PublicBridge, PrivateChainBridge::removeReleaser` - cache `releasers.length`
* `PublicBridge, PrivateChainBridge::payReleaseFee` - cache `releaseFee, releasers.length`
* `PublicBridge, PrivateChainBridge::lockTokens` - cache `bridgeFee` prior to the `if` check and use cached value, cache `bridgeFeeReceiver` inside the `if` check
* `PublicBridge, PrivateChainBridge::signRelease` - cache `signatureCount[txHash]++`
* `PublicBridge::_releaseTokens` - cache `token, vault`
* `PrivateChainBridge::_releaseTokens` - cache `vault`
* `PublicBridge, PrivateChainBridge::_processPendingReleases` - cache `releases.length`
* `PublicBridge, PrivateChainBridge::_cleanPendingReleases` - cache `releases.length, pendingRecipients.length`
* `PublicBridge, PrivateChainBridge::forceProcessPendingRelease` - cache `release.recipient, release.amount`
* `PublicBridge, PrivateChainBridge::acceptOwnership` - cache `pendingOwner`
* `Token::confirmOwnership` - instead of modifier `only(pendingOwner)`, use an internal function that returns `pendingOwner`, then use that cached return value to set `owner` and emit event `TransferOwnership`

**BridgeX:**
Fixed in commit [57230de](https://github.com/NerdUnited-NodeGovernance/audit-2026-03-bridgex/commit/57230de56c6d0b1f5c23e2c2042985dee9029abe).

**Cyfrin:** Verified.

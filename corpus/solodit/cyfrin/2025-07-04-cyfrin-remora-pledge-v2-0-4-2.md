---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-4-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Cache identical storage reads
vuln_class: []
---

# Cache identical storage reads

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** Reading from storage is expensive, cache identical storage reads to prevent re-reading the same storage values multiple times.

`PledgeManager.sol`:
```solidity
// cache `stablecoinDecimals` in `_fixDecimals`
307:            stablecoinDecimals < 6
308:                ? value / (10 ** (6 - stablecoinDecimals))
309:                : value * (10 ** (stablecoinDecimals - 6));

// cache `propertyToken` in `_verifyDocumentSignature`
316:        (bool res, ) = IRemoraRWAToken(propertyToken).hasSignedDocs(signer);
318:            IRemoraRWAToken(propertyToken).verifySignature(
```

`TokenBank.sol`:
```solidity
// cache `developments.length` in `removeToken`
152:        for (uint i = 0; i < developments.length; ++i) {
154:            address end = developments[developments.length - 1];

// cache `developments.length` in `viewAllFees`, claimAllFees
226:        for (uint i = 0; i < developments.length; ++i)
233:        for (uint i = 0; i < developments.length; ++i) {
```

`LockUpManager.sol`:
```solidity
// cache `userData.endInd` in `availableTokens`, `_unlockTokens`
117:        for (uint16 i = userData.startInd; i < userData.endInd; ++i) {
146:        for (uint16 i = userData.startInd; i < userData.endInd; ++i) {
```

**Remora:** Fixed in commit [6602423](https://github.com/remora-projects/remora-smart-contracts/commit/66024232cfea24b69bd055086f8088d40f3d1d4a).

**Cyfrin:** Verified.

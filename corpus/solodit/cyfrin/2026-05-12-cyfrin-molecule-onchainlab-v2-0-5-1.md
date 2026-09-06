---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-5-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: Redundant default initialization to `0`
vuln_class: []
---

# Redundant default initialization to `0`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** Solidity initializes integer locals to zero. Explicit `= 0` adds a `PUSH0` (or `PUSH1 0x00`) and a store/assign that the optimizer may eliminate but does not guarantee to remove on every code path; the source remains noise. Multiple loop iterators and counters in scope contain the explicit `= 0` initializer.

```solidity
src/ERC7484Registry/ERC7484Registry.sol
153:        uint256 validCount = 0;
154:        for (uint256 i = 0; i < attesters.length; i++) {
169:        uint256 validCount = 0;
171:        for (uint256 i = 0; i < attesters.length; i++) {
195:        uint256 validCount = 0;
197:        for (uint256 i = 0; i < attesters.length; i++) {
228:        for (uint256 i = 1; i < attesters.length; i++) {  // i=1 is intentional, not flagged

src/identity/OdfCoAttestVerifier.sol
82:        for (uint256 i = 0; i < 2; i++) {

src/factory/OnChainLabFactory.sol
161:        for (uint256 i = 0; i < len; i++) {
172:        for (uint256 i = 0; i < len; i++) {

src/identity/MoleculeOclDidRegistry.sol
201:        for (uint256 i = 0; i < len; i++) {
```

**Recommended Mitigation:** Drop the explicit `= 0`:

```solidity
uint256 validCount;
for (uint256 i; i < attesters.length; ++i) { ... }
```

(Line 228 of ERC7484Registry is `i = 1` and should remain - it intentionally starts at index 1 to compare with index 0.)

**Molecule:** Fixed in [a6438f1](https://github.com/moleculeprotocol/onchainlabs/commit/a6438f1).

**Cyfrin:** Verified.

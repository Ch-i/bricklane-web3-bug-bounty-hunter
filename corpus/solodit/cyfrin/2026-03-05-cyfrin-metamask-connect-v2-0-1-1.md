---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-05-cyfrin-metamask-connect-v2-0-1-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-03-05T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-05-cyfrin-metamask-connect-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-05-cyfrin-metamask-connect-v2-0
title: eciesjs major version mismatch between dApp SDK and mobile wallet creates untested
  cryptographic interoperability risk
vuln_class: []
---

# eciesjs major version mismatch between dApp SDK and mobile wallet creates untested cryptographic interoperability risk

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-05-cyfrin-metamask-connect-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-05-cyfrin-metamask-connect-v2.0.md)_

---

**Description:** The dApp SDK `connect-multichain` uses eciesjs **v0.4.16** while MetaMask Mobile uses eciesjs **v0.3.21**. Additionally, `eciesjs v0.3.21` declares a dependency on `secp256k1@^5.0.1`, but a Yarn `resolutions` override in MetaMask Mobile force-pins it to **v4.0.4**, a full major version behind what eciesjs expects.

```
eciesjs@npm:^0.3.15":
  version: 0.3.21
  dependencies:
    futoin-hkdf: "npm:^1.5.3"
    secp256k1: "npm:^5.0.1
```
While the basic API surface overlaps, there are subtle differences in default hash functions, error handling, and constant-time guarantees between v4 and v5.

**Impact:**
- Silent decryption failures or degraded cipher parameters if envelope formats diverge
- Potential subtle cryptographic behavior differences from the `secp256k1` downgrade
- Difficult to reproduce bugs that only surface in `cross-platform` (dApp ↔ wallet) communication

**Recommended Mitigation:**
- Align both sides on the **same** eciesjs major version (preferably 0.4.x)
- Remove or update the `secp256k1` resolution override so eciesjs gets the version it declares
- Add a CI check or integration test that verifies cross-platform encrypt/decrypt round-trips between the dApp SDK and mobile wallet

**Metamsk:**
Fixed in commit [f262f7](https://github.com/MetaMask/metamask-mobile/commit/f262f7c15251aee6f1c1734c28fa60aa4f19e13a).

**Cyfrin:** Verified.

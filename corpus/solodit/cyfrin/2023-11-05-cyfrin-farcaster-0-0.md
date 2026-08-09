---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-05-cyfrin-farcaster-0-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-11-05T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-05-cyfrin-farcaster.md
tags:
- firm:cyfrin
- report:2023-11-05-cyfrin-farcaster
title: A signer can't cancel his signature before a deadline.
vuln_class: []
---

# A signer can't cancel his signature before a deadline.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-05-cyfrin-farcaster.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-05-cyfrin-farcaster.md)_

---

**Severity:** Medium

**Description:** After signing a signature, a signer might want to cancel it for some reason. While checking other protocols, a signer can cancel by increasing his nonce.
In this protocol, we inherit from OpenZeppelin's [Nonces](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/Nonces.sol) contract and there are no ways to cancel the signature before a deadline.

**Impact:** Signers can't invalidate their signatures when they want.

**Recommended Mitigation:** Recommend adding a function like `increaseNonce()` to invalidate the past signatures.

**Client:**
Fixed by adding a base `Nonces` contract that exposes an external `useNonce()` function, enabling the caller to increment
their nonce. Commit: [`0189a1f`](https://github.com/farcasterxyz/farcaster-contracts-private/commit/0189a1fd308a5976ecdfbce2765b6d7a953eb80f)

**Cyfrin:** Verified.

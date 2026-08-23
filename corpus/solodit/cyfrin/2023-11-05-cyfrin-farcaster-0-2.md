---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-05-cyfrin-farcaster-0-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-11-05T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-05-cyfrin-farcaster.md
tags:
- firm:cyfrin
- report:2023-11-05-cyfrin-farcaster
title: '`IdRegistry.transfer/transferFor()` might be revoked by a recovery address.'
vuln_class: []
---

# `IdRegistry.transfer/transferFor()` might be revoked by a recovery address.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-05-cyfrin-farcaster.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-05-cyfrin-farcaster.md)_

---

**Severity:** Medium

**Description:** In every `fid`, there exists an owner and a recovery address, each possessing identical authority, enabling either one to modify the other.
But while transferring the `fid`, it just changes the owner and this scenario might be possible.

- Consider Bob with a `fid(owner, recovery)` intending to sell it.
- After receiving some funds, he transfers his `fid` to an honest user using `transfer()`.
- When the honest user is going to update the recovery address, Bob calls `recover()` by front running and seizes the account.
- In contrast to ERC721, a recovery address acts like an approved user for the NFT, empowered to change ownership at any moment. Notably, this authority is cleared during the [transfer](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol#L252) to prevent subsequent updates by any prior approvals.

**Impact:** `IdRegistry.transfer/transferFor()` might be revoked by a recovery address.

**Recommended Mitigation:** Recommend adding a function like `transferAll()` to update both `owner/recovery`.

**Client:**
Fixed by adding `transferAndChangeRecovery` and `transferAndChangeRecoveryFor` to `IdRegistry`. Commit: [`d389f9f`](https://github.com/farcasterxyz/farcaster-contracts-private/commit/d389f9f9e102ea1706f115b0aba2c7e429ba3e9a)

**Cyfrin:** Verified.

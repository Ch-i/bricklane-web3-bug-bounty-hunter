---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-05-cyfrin-farcaster-0-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-11-05T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-05-cyfrin-farcaster.md
tags:
- firm:cyfrin
- report:2023-11-05-cyfrin-farcaster
title: In `IdRegistry`, a recovery address might be updated unexpectedly.
vuln_class: []
---

# In `IdRegistry`, a recovery address might be updated unexpectedly.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-05-cyfrin-farcaster.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-05-cyfrin-farcaster.md)_

---

**Severity:** Medium

**Description:** There are 2 functions to update a recovery address, `changeRecoveryAddress()` and `changeRecoveryAddressFor()`.
As `changeRecoveryAddress()` doesn't reset a pending signature that would be used in `changeRecoveryAddressFor()`, the below scenario would be possible.

- Alice decided to set a recovery as Bob and created a signature for that.
- But before calling `changeRecoveryAddressFor()`, Alice noticed Bob was not a perfect fit and changed the recovery address to another one by calling `changeRecoveryAddress()` directly.
- But Bob or anyone calls `changeRecoveryAddressFor()` after that and Bob can change the owner as well.

Of course, Alice could delete the signature by increasing her nonce but it's not a good approach for users to be allowed to use the previous signature.

**Impact:** A recovery address might be updated unexpectedly.

**Recommended Mitigation:** We should include the current recovery address in the recovery signature.
Then the previous signature will be invalidated automatically after changing the recovery.

**Client:**
Fixed by adding the current recovery address to `CHANGE_RECOVERY_ADDRESS_TYPEHASH`. Commit: [`7826446`](https://github.com/farcasterxyz/farcaster-contracts-private/commit/7826446c172d2038ab7b3eeb3073c3a7233061df)

**Cyfrin:** Verified.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-06-cyfrin-wlfi-unlock-v2-0-2-6
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-05-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-06-cyfrin-wlfi-unlock-v2-0
title: '`WorldLibertyFinancialV3::electVestingUpdate` signature has no nonce and no
  deadline, making replay protection purely state-based'
vuln_class: []
---

# `WorldLibertyFinancialV3::electVestingUpdate` signature has no nonce and no deadline, making replay protection purely state-based

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-06-cyfrin-wlfi-unlock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md)_

---

**Description:** `WorldLibertyFinancialV3::electVestingUpdate` verifies an EIP-712 signature over `Election(address account)`. The struct contains only the `account` field — there is no `nonce`, no `deadline`, no version marker:

```solidity
// WorldLibertyFinancialV3.sol
bytes32 private constant ELECTION_TYPEHASH = keccak256("Election(address account)");

function electVestingUpdate(bytes calldata _signature) external {
    address account = _msgSender();
    bytes32 hash = _hashTypedDataV4(keccak256(abi.encode(ELECTION_TYPEHASH, account)));
    if (authorizedSigner() != ECDSA.recover(hash, _signature)) {
        revert InvalidSignature();
    }
    _electVestingUpdate(account);
}
```

Once a signature is issued by `authorizedSigner`, it remains valid indefinitely until either:

- The user's Registry category transitions to 45 or 47 — at which point `_electVestingUpdate` reverts with `ElectionAlreadyPerformed`, providing state-based single-use semantics.
- The owner rotates `authorizedSigner` via `ownerSetAuthorizedSigner` — at which point the old sig no longer recovers to the new authorized address and `ECDSA.recover` produces a mismatch.

**Recommended Mitigation:** Consider adding nonce and deadline to the `Election` typehash.

**WLFI:** Fixed in commit [1430e24](https://github.com/worldliberty/usd1-protocol/commit/1430e245349795921bebe275f6bd1d835d9f8fa3).

**Cyfrin:** Verified.

\clearpage

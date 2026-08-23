---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-3-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: '`CUSTODIAN_ROLE` is granted/revoked but never gates any function'
vuln_class: []
---

# `CUSTODIAN_ROLE` is granted/revoked but never gates any function

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** `Minter` declares `CUSTODIAN_ROLE` and manages it through `requestCustodianChange`/`setCustodian`, but no function uses `onlyRole(CUSTODIAN_ROLE)`. The role is dead code - the custodian is used only as the destination in `transferToCustody` (which is gated by `OPERATOR_ROLE`, not `CUSTODIAN_ROLE`). Readers will assume this role grants privileges it does not. Related drift risk: `transferToCustody` uses `$.custodian` storage, not the role set, so the custodian address and role membership can diverge - off-chain tooling treating the role as meaningful is misled.

```solidity
issuance/src/minter/Minter.sol
44:    bytes32 public constant CUSTODIAN_ROLE = keccak256(\"CUSTODIAN_ROLE\");
```

Source: `issuance/src/minter/Minter.sol:44, 198, 344-346`.

**Recommended Mitigation:** Either:
- Remove the role entirely (and the grant/revoke bookkeeping), OR
- Gate the recipient of `transferToCustody` with `hasRole(CUSTODIAN_ROLE, recipient)` so the role has operational meaning, OR
- Add a function that actually requires `onlyRole(CUSTODIAN_ROLE)`.

**Syntetika:** Fixed in commit [`27bcdf8`](https://github.com/SyntetikaLabs/monorepo/commit/27bcdf8e7b6bf03d508fe959d1d953955d564527)

**Cyfrin:** Verified. `CUSTODIAN_ROLE` removed.

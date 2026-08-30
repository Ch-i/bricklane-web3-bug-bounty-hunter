---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-3-11
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: '`Minter::ownerMint` bypasses whitelist requirement and increases `totalDeposits`
  without actually transferring any tokens'
vuln_class: []
---

# `Minter::ownerMint` bypasses whitelist requirement and increases `totalDeposits` without actually transferring any tokens

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** The regular functions `Minter::mint, redeem` enforce whitelist requirements and always transfer or burn tokens when incrementing or decrementing `totalDeposits`.

In contrast the admin function `Minter::ownerMint`:
* doesn't enforce whitelist requirements on `addressTo`
* increments `totalDeposits` without actually transferring any tokens into the contract

**Impact:** Misuse of this function can cause:
* tokens to be minted to a non-whitelisted address
* corruption of `totalDeposits` which can become different to the actual amount of tokens in the contract
* the admin could mint themselves infinite `hBTC` tokens which they could then use to drain pair tokens from any decentralized liquidity pools

**Recommended Mitigation:** Ideally `Minter::ownerMint` would require the admin to supply sufficient `baseAsset` tokens to the contract.

**Syntetika:**
Acknowledged; this is the intended functionality of the `ownerMint` function.

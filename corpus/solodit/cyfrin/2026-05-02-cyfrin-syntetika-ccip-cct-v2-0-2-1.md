---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-2-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: '`Minter::ownerMint` inverted waiting-period check enables single-tx unbacked
  mint; chained with self-whitelist drains all `Minter` baseAsset'
vuln_class: []
---

# `Minter::ownerMint` inverted waiting-period check enables single-tx unbacked mint; chained with self-whitelist drains all `Minter` baseAsset

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** The 2-step admin pattern is intended to force `requiredWaitingPeriod` (>=1 day) between `requestOwnerMint` and `ownerMint`. All other 2-step sites in Minter use `timestamp + requiredWaitingPeriod <= block.timestamp`; `ownerMint` alone uses `>`:

```solidity
require(
    $.ownerMintRequest.timestamp + $.requiredWaitingPeriod >
        block.timestamp,
    WaitingPeriodNotElapsed()
);
```

The operator is inverted: the require passes while the waiting period has NOT yet elapsed and reverts afterwards. A malicious admin (or leaked admin key) can call `requestOwnerMint(amount, attacker)` and `ownerMint()` in the same block. Chained with `Minter::whitelistAddress` (single-step admin) and `Minter::redeem` (whitelist-gated on msg.sender only), an attacker with `DEFAULT_ADMIN_ROLE` drains in one block: (1) `requestOwnerMint(huge, attacker)` + `ownerMint()`; (2) `whitelistAddress(attacker, true)`; (3) `Minter::redeem(amount)` - `spender==from` skips allowance; `baseAsset.safeTransfer(attacker, amount)` drains all Minter baseAsset reserves.

Source: `issuance/src/minter/Minter.sol:232-246`.

**Impact:** Single-tx drain of all on-chain baseAsset held in Minter plus permanent inflation of HilSyntheticToken supply under a compromised admin key. Directly violates client's stated 2-step invariant. Off-chain custodian-held baseAsset is unaffected, but the 1:1 peg is destroyed instantly. Also breaks the honest flow: after the intended 1-day wait, the same call reverts permanently until a fresh request.

**Recommended Mitigation:**
```solidity
require(
    $.ownerMintRequest.timestamp != 0 &&
    $.ownerMintRequest.timestamp + $.requiredWaitingPeriod <= block.timestamp,
    WaitingPeriodNotElapsed()
);
```

Also validate `to != address(0)` and `amount > 0` in `requestOwnerMint`. Note: the per-site fix patches the 2-step flow itself, but the architectural grantRole bypass separately makes the 2-step surface bypassable via direct `grantRole`.

**Syntetika:** Fixed in commit [`dc0cfc7`](https://github.com/SyntetikaLabs/monorepo/commit/dc0cfc76a63896f783759a23fea548ec50ca51d1)

**Cyfrin:** Verified.

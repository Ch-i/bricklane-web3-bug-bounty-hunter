---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-05-cyfrin-securitize-evm-async-vault-v2-0-4-2
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-08-05T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-05-cyfrin-securitize-evm-async-vault-v2-0
title: Pack the tolerance with the cached token decimal fields
vuln_class: []
---

# Pack the tolerance with the cached token decimal fields

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md)_

---

**Description:** `VaultStorage` leaves the two cached decimal fields in a mostly empty slot, then places the two-byte `navPriceTolerance` after the `operators` mapping, forcing it into a new slot. Moving the tolerance immediately after the decimal fields makes all three values share a slot. The layout uses slots 0 through 17 before the move and slots 0 through 16 after it, reducing the layout from 18 to 17 slots. This saves one initialized storage slot per newly deployed vault and can make the tolerance read warm after the decimal reads in NAV checks.

```solidity
contracts/base/AsyncFundVaultStorage.sol
154:        // ── Token metadata cache ───────────────────────────────────────────
155:        /// @dev DS Token decimal count, cached from `dsToken.decimals()` at initialisation.
156:        uint8 dsDecimals;
157:        /// @dev Liquidity token decimal count, cached from `liquidityToken.decimals()` at
158:        ///      initialisation.  Required for WAD navPrice conversion arithmetic.
159:        uint8 liquidityDecimals;
161:        // ── Operators ─────────────────────────────────────────────────────
162:        /// @dev operators[controller][operator] = approved.
163:        mapping(address controller => mapping(address operator => bool approved)) operators;
165:        // ── NAV price tolerance ────────────────────────────────────────────
169:        uint16 navPriceTolerance;
```

**Recommended Mitigation:** Move `navPriceTolerance` directly after `liquidityDecimals` in `contracts/base/AsyncFundVaultStorage.sol` so all three values occupy the same slot:

```solidity
uint8 dsDecimals;
uint8 liquidityDecimals;
uint16 navPriceTolerance;
mapping(address controller => mapping(address operator => bool approved)) operators;
```

**Securitize:** Fixed in commit [bc377f3](https://github.com/securitize-io/bc-async-ramp-sc/commit/bc377f35f29784d8f089a71833c3d6d835e43122).

**Cyfrin:** Verified.

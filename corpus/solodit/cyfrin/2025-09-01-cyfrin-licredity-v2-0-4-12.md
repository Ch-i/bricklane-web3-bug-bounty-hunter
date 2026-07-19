---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-4-12
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-09-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-01-cyfrin-licredity-v2-0
title: Fungible array can contain zero-balance entries
vuln_class: []
---

# Fungible array can contain zero-balance entries

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-01-cyfrin-licredity-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md)_

---

**Description:** The `addFungible` function allows adding fungibles with zero amounts, while `removeFungible` correctly removes fungibles when balance reaches zero. This creates an inconsistency where the fungibles array can legitimately contain entries with zero balance in `fungibleStates`.

**Impact:** Edge case that creates state inconsistency.

**Proof of Concept:** ❌Violated: https://prover.certora.com/output/52567/0586939d1ed34d3aa9e7292ab15eb1f9/?anonymousKey=07ffaae5e729a887ef83913c7d3e25027f3f51a2

```solidity
// VS-LI-08: Fungibles in array must have corresponding fungibleStates with non-zero balance
// For every fungible in the fungibles array, there must be a corresponding fungibleStates entry with non-zero balance
invariant fungiblesHaveNonZeroBalance(env e)
    forall uint256 positionId. forall uint8 i.
        i < ghostLiPositionFungiblesLength[positionId]
            => ghostLiPositionFungibleStatesBalance112[positionId][ghostLiPositionFungibles[positionId][i]] != 0
filtered { f -> !EXCLUDED_FUNCTION(f) } { preserved with (env eFunc) { SETUP(e, eFunc); } }
```

**Recommended Mitigation:**
```diff
diff --git a/core/src/types/Position.sol b/core/src/types/Position.sol
index 929f27e..d346262 100644
--- a/core/src/types/Position.sol
+++ b/core/src/types/Position.sol
@@ -44,6 +44,9 @@ library PositionLibrary {
         FungibleState state = self.fungibleStates[fungible];

         if (state.index() == 0) {
+
+            require(amount != 0); // @certora fix for fungiblesHaveNonZeroBalance
+
             // add a fungible to the fungibles array
             assembly ("memory-safe") {
                 let slot := add(self.slot, FUNGIBLES_OFFSET)
```

✅Passed (after the fix): https://prover.certora.com/output/52567/d54bd10fcbb1482fb2392dbe9a4a122f/?anonymousKey=410cd2a910ca4d91e2ec8d457aff189648ade968

**Licredity:** Fixed in [PR#67](https://github.com/Licredity/licredity-v1-core/pull/67/files), commit [`7eba957`](https://github.com/Licredity/licredity-v1-core/commit/7eba95743ed72eed62e826cc168edd7ca4becb92). Our preference is to not disallow operations that is harmless though useless. So we prevent state change (other than event) but do not revert.

**Cyfrin:** Verified. No state change if `amount` is zero.

\clearpage

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-24-cyfrin-avant-requestmanagerv2-v2-0-1-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-06-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-24-cyfrin-avant-requestmanagerv2-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-24-cyfrin-avant-requestmanagerv2-v2-0
title: '`README.md` documentation mismatches: stale and inaccurate references disagree
  with the code and docs'
vuln_class: []
---

# `README.md` documentation mismatches: stale and inaccurate references disagree with the code and docs

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-24-cyfrin-avant-requestmanagerv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-24-cyfrin-avant-requestmanagerv2-v2.0.md)_

---

**Description:** `README.md` contains several statements that disagree with the in-scope contract source and the supplied project docs (`AUDIT_NOTES.md`, `RFP-RequestsManagerV2-external-audit.md`). The inaccuracies mis-state burn pricing, fees, the request-counter offset, the price bounds, and admin powers in ways a reader or integrator would act on.

1. **`README.md:82, 88`** - burn settlement is described as using only the stored request-time price.

   The README states `completeBurn` _"uses this stored price, making the withdrawal amount immune to post-request price changes"_ (`README.md:82`) and that burn prices _"are locked at request time and cannot change"_ (`README.md:88`). The code settles at `min(lockedPrice, currentPrice)` (`src/RequestsManagerV2.sol:406-409`): the stored price is a ceiling only, so a price fall after the request lowers the payout. `AUDIT_NOTES.md:71` and `RFP-RequestsManagerV2-external-audit.md:83` both state the redeemer bears a NAV fall.

   **Recommended:** state that burns settle at `min(lockedPrice, currentPrice)` - the request-time price is a ceiling, not a fixed settlement price, and a price decrease is borne by the redeemer.

2. **`README.md:145`** - the burn formula omits the `min(lockedPrice, currentPrice)`.

   The formula table gives `withdrawalAmount = (burnAmount * price / PRECISION) * (PRECISION - burnFee) / PRECISION` with a generic `price`. The code uses `price = min(lockedPrice, currentPrice)` and the locked `request.fee`, not the live `burnFee` (`src/RequestsManagerV2.sol:409, 412-413`).

   **Recommended:** replace `price` with `min(lockedPrice, currentPrice)` and note the fee is the value locked at request time.

3. **`README.md:125`** - `setBurnFee` is described as retroactive on pending burns.

   The trust model lists _"Change fees retroactively on pending burns (`setBurnFee`)"_. The code locks the burn fee into the `BurnRequest` at request time (`src/RequestsManagerV2.sol:322, 331`) and `completeBurn` consumes `request.fee` (`src/RequestsManagerV2.sol:403`); the `setBurnFee` NatSpec states it applies _"for new requests; pending burns keep the fee locked at request time"_ (`src/RequestsManagerV2.sol:196-197`). The RFP records the retroactive-burn-fee issue as fixed (`RFP-RequestsManagerV2-external-audit.md:273`). The live fee is the mint fee, not the burn fee.

   **Recommended:** remove the retroactive-burn-fee claim; the only live fee is `setMintFee`, applied at completion.

4. **`README.md:118`** - the V2 request-counter start value is wrong.

   The README says counters start at 10,000 and that V1 has _"fewer than 10,000 existing orders"_. The code initializes both counters to `INITIAL_COUNTER = 100_000` (`src/RequestsManagerV2.sol:47, 127-128`); `RFP-RequestsManagerV2-external-audit.md:121` and `AUDIT_NOTES.md:83` both state 100,000.

   **Recommended:** correct the value to 100,000 and update the dependent order-count statement.

5. **`README.md:133, 180`** - the price bounds are presented as fixed guarantees.

   The README implies the bounds are enforced at the +5% upper / -33% lower figures (_"each update is constrained to"_ those values). They are settable parameters: `PriceStorage::setUpperBoundPercentage, setLowerBoundPercentage` accept any value in `(0, 1e18]` (`src/PriceStorage.sol:56-72`), and the RFP notes the figures derive from test configuration with production values TBD (`RFP-RequestsManagerV2-external-audit.md:145`).

   **Recommended:** describe the bounds as configurable parameters rather than presenting the test-config values as enforced guarantees.

6. **`README.md:170`** - the role-permissions table omits two admin setters.

   The table lists `setBurnRequestTTL` but not `setMintRequestTTL` (`src/RequestsManagerV2.sol:174`) or `setBurnCancelWindow` (`src/RequestsManagerV2.sol:183`), both `DEFAULT_ADMIN_ROLE` setters present in the code.

   **Recommended:** add `setMintRequestTTL` and `setBurnCancelWindow` to the `DEFAULT_ADMIN_ROLE` row.

7. **`README.md:92-104`** - the "New features" section omits the mint TTL and the burn cancel window.

   The section documents the burn TTL but not `mintRequestTTL` (enforced in `completeMint`, `src/RequestsManagerV2.sol:278`) or `burnCancelWindow` (enforced in `cancelBurn`, `src/RequestsManagerV2.sol:367`), both new V2 mechanisms.

   **Recommended:** document `mintRequestTTL` and `burnCancelWindow` alongside the existing burn TTL entry.

**Avant:** Fixed in commit [a97fcaf](https://github.com/Avant-Protocol/Avant-Contracts-Max/commit/a97fcaf42cb5511690a20864c778e79cc07fa397).

**Cyfrin:** Verified.

\clearpage

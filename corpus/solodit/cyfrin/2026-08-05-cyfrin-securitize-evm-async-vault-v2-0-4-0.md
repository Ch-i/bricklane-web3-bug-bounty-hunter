---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-05-cyfrin-securitize-evm-async-vault-v2-0-4-0
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
title: Cache request balances that are checked before an additive update
vuln_class: []
---

# Cache request balances that are checked before an additive update

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md)_

---

**Description:** The request and reassignment flows read a pending-balance mapping entry to determine whether to add a generation to a controller list, then read the same entry again for the additive update. Cache the initial value and perform a single calculated write to avoid the repeat warm mapping read on the successful path.

```solidity
contracts/AsyncFundVault.sol
389:        if ($.pendingDepositAssets[genId][controller] == 0) {
395:        $.pendingDepositAssets[genId][controller] += assets;
585:        if ($.pendingRedeemShares[genId][controller] == 0) {
591:        $.pendingRedeemShares[genId][controller] += shares;

contracts/base/AsyncFundVaultAdmin.sol
258:        bool toHadNoPriorClaim = $.pendingDepositAssets[generationId][to] == 0;
260:        $.pendingDepositAssets[generationId][to] += amount;
287:        bool toHadNoPriorClaim = $.pendingRedeemShares[generationId][to] == 0;
289:        $.pendingRedeemShares[generationId][to] += shares;
```

**Recommended Mitigation:** In `contracts/AsyncFundVault.sol`, load each pending balance into a local before the zero check, use that value for the list decision, and assign the computed sum rather than using `+=`:

```solidity
uint256 pendingAssets = $.pendingDepositAssets[genId][controller];
if (pendingAssets == 0) {
    if ($.controllerDepositGenerations[controller].length >= MAX_OUTSTANDING_GENERATIONS) {
        revert TooManyOutstandingGenerations();
    }
    $.controllerDepositGenerations[controller].push(genId);
}
$.pendingDepositAssets[genId][controller] = pendingAssets + assets;
```

Apply the same cache-and-single-write pattern to the redemption request site. For `reassignClaimableDeposit` and `reassignClaimableRedemption`, preserve the current same-address semantics: because the source slot is zeroed before the destination is incremented, any destination caching must re-read after the zeroing step or apply only when `from != to`.

**Securitize:** Fixed in commit [7574b36](https://github.com/securitize-io/bc-async-ramp-sc/commit/7574b36809cfadfad9e15f35b4e76d66f4bbed05).

**Cyfrin:** Verified.

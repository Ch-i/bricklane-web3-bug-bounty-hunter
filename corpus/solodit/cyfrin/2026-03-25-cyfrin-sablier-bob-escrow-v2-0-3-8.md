---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-3-8
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: ETH sent with adapter vault redemption is trapped in `SablierBob`
vuln_class: []
---

# ETH sent with adapter vault redemption is trapped in `SablierBob`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** `SablierBob::redeem` is declared `payable` unconditionally, but only the non-adapter path handles `msg.value`. When a user calls `redeem` on an adapter vault with `msg.value > 0` (`SablierBob.sol:290-373`), the adapter path (`SablierBob.sol:326-345`) never checks, forwards, or refunds the ETH:

```solidity
if (address(vault.adapter) != address(0)) {
    // Adapter path: handles ERC-20 yield fee
    // msg.value is NEVER checked, forwarded, or refunded
}
else {
    // Non-adapter path: checks msg.value >= minFeeWei, forwards to comptroller
}
```

The ETH enters `SablierBob` via the `payable` function but has no code path to return to the user. It remains in the contract until someone calls `transferFeesToComptroller` (inherited from `Comptrollerable`), which sweeps the contract's entire ETH balance to the comptroller — not back to the user who sent it.

**Impact:** Users who mistakenly send ETH when redeeming from adapter vaults permanently lose that ETH. While `transferFeesToComptroller` can recover the ETH to the comptroller, the user who sent it has no claim to it. The likelihood is low since adapter vaults don't require ETH fees, but the `payable` modifier provides no indication that ETH is unnecessary and will be lost.

**Recommended Mitigation:** Revert early in the adapter path if `msg.value > 0`:

```solidity
if (address(vault.adapter) != address(0)) {
    if (msg.value > 0) {
        revert Errors.SablierBob_UnexpectedNativeToken(vaultId);
    }
    // ... rest of adapter logic
}
```

**Sablier:** Fixed in commit [44b6bf1](https://github.com/sablier-labs/lockup/commit/44b6bf10f5e9e126b808f8bfd20a098d1275063f).

**Cyfrin:** Verified.

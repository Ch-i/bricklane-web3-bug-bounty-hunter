---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-3-16
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Enforce that `StakingVault::decimals` is greater or equal to the underlying
  asset decimals
vuln_class: []
---

# Enforce that `StakingVault::decimals` is greater or equal to the underlying asset decimals

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** [EIP4626](https://eips.ethereum.org/EIPS/eip-4626) states:
> Although the convertTo functions should eliminate the need for any use of an EIP-4626 Vault’s decimals variable, it is still strongly recommended to mirror the underlying token’s decimals if at all possible, to eliminate possible sources of confusion and simplify integration across front-ends and for other off-chain users.

And this set of [vault property tests](https://github.com/crytic/properties/blob/main/contracts/ERC4626/properties/SecurityProps.sol#L8-L11) enforce that the vault's decimals are greater or equal to the underlying asset decimals:
```solidity
        assertGte(
            vault.decimals(),
            asset.decimals(),
            "The vault's share token should have greater than or equal to the number of decimals as the vault's asset token."
        );
```

**Recommended Mitigation:** In `StakingVault::constructor`, revert if `IERC20Metadata(_asset).decimals() > decimals()`.

**Syntetika:**
Fixed in commit [ac97972](https://github.com/SyntetikaLabs/monorepo/commit/ac97972d762392dc8465fa70c718fa78615636ff) by enforcing decimal equality per the EIP4626 standard recommendation.

**Cyfrin:** Verified.

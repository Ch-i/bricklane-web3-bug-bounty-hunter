---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-5-6
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: Cache storage to prevent identical storage reads
vuln_class: []
---

# Cache storage to prevent identical storage reads

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** Reading from storage is expensive; cache storage to prevent identical storage reads:
* `SablierBob::exitWithinGracePeriod, redeem` - `vault.shareToken`, potentially also `vault.adapter` if the most likely case is non-zero
* `SablierBob::redeem` - `comptroller` in the branch where no vault adapter exists if `minFeeWei` is likely to be > 0
* `SablierBob::unstakeTokensViaAdapter` - `vault.adapter`
* `SablierBob::onShareTransfer` - `_vaults[vaultId].adapter` if the most likely case is non-zero

**Sablier:** Fixed in commit [7d9ac86](https://github.com/sablier-labs/lockup/commit/7d9ac86a6edc85383b1fc9b58fdfbaf78a8f1cb1).

**Cyfrin:** Verified.

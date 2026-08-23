---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-3-2
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
title: '`StakingVault::setEarlyExitFeeRecipient` defaults to `address(this)` and permits
  self-target - fees silently boost share price'
vuln_class: []
---

# `StakingVault::setEarlyExitFeeRecipient` defaults to `address(this)` and permits self-target - fees silently boost share price

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** Default fee recipient is the vault itself. Early-exit fees returned to the vault via `tokensHolder.withdraw($.earlyExitFeeRecipient, fee)` increase `balanceOf(vault)` and therefore `totalAssets()` instantly - bypassing the vesting mechanism and inflating share price for remaining holders. Absent admin action, all early-exit fees are ploughed back silently.

Source: `issuance/src/vault/StakingVault.sol:126, 175-182`.

**Recommended Mitigation:** Either document the self-recycling behaviour, or `require(newRecipient != address(this))` and initialize with a treasury address.

**Syntetika:** Fixed in commit [`cdd5107`](https://github.com/SyntetikaLabs/monorepo/commit/cdd510713a7a5a4d785038c52897ab83efe310ec)

**Cyfrin:** Verified.

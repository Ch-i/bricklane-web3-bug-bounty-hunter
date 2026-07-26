---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-3-13
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: Solidity compiler version and toolchain configuration drift across the repo
vuln_class: []
---

# Solidity compiler version and toolchain configuration drift across the repo

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** Grouping of compiler-version and toolchain configuration inconsistencies across the repo.

---

**1. Pragma drift across in-scope contracts**

Different files pin different pragmas: `^0.8.26` for most files; `^0.8.20` for `TokensHolder`; `^0.8.19` for `StakingVault` and `Distributor`. Foundry configures `solc_version = "0.8.26"` so all files compile there, but the floor pragmas silently allow building against older versions that miss features used elsewhere.

**Recommended:** Align to `^0.8.26` across all in-scope files so static analyzers and downstream tooling consistently target the same version.

---

**2. Hardhat vs Foundry version mismatch; Hardhat optimizer disabled**

The Hardhat config compiles deposit-registry contracts with `0.8.28`, while the issuance Foundry config uses `0.8.26`. Hardhat config does NOT specify an optimizer - disabled by default, producing larger, more expensive bytecode.

**Recommended:** Enable the optimizer in `hardhat.config.ts` and align the Solidity version with `foundry.toml`:

```ts
solidity: {
  version: "0.8.26",
  settings: {
    optimizer: { enabled: true, runs: 200 },
    viaIR: true,
  },
},
```

---

**Syntetika:** Fixed in commit [`564be0`](https://github.com/SyntetikaLabs/monorepo/commit/564be06d036837354d391f216060d774d6ce5b20)

**Cyfrin:** Verified.

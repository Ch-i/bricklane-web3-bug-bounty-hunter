---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-17-cyfrin-quantamm-v1-2-3-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-12-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md
tags:
- firm:cyfrin
- report:2024-12-17-cyfrin-quantamm-v1-2
title: '`TODO`s left in rule parameter descriptions'
vuln_class: []
---

# `TODO`s left in rule parameter descriptions

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-17-cyfrin-quantamm-v1.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md)_

---

**Description:** The three rules [`AntimomentumUpdateRule`](https://github.com/QuantAMMProtocol/QuantAMM-V1/blob/7213401491f6a8fd1fcc1cf4763b15b5da355f1c/pkg/pool-quantamm/contracts/rules/AntimomentumUpdateRule.sol#L17), [`MinimumVarianceUpdateRule`](https://github.com/QuantAMMProtocol/QuantAMM-V1/blob/7213401491f6a8fd1fcc1cf4763b15b5da355f1c/pkg/pool-quantamm/contracts/rules/MinimumVarianceUpdateRule.sol#L15) and [`MomentumUpdateRule`](https://github.com/QuantAMMProtocol/QuantAMM-V1/blob/7213401491f6a8fd1fcc1cf4763b15b5da355f1c/pkg/pool-quantamm/contracts/rules/MomentumUpdateRule.sol#L15) have `TODO`s left in their parameter descriptions.

Consider finalizing the descriptions of these parameters.

**QuantAMM:** Fixed in [`e3e0d5e`](https://github.com/QuantAMMProtocol/QuantAMM-V1/commit/e3e0d5eab5f81d2141ce69daffb249c223385b2f), [`8c3a4f3`](https://github.com/QuantAMMProtocol/QuantAMM-V1/commit/8c3a4f3df43ba8731808c226b2fe4eb68b3e7c8b), [`f56796e`](https://github.com/QuantAMMProtocol/QuantAMM-V1/commit/f56796ee75615a28c14c3678d984d5b55d3cf864)

**Cyfrin:** Verified.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-26-cyfrin-eulerswap-v2-0-0-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-05-26T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-26-cyfrin-eulerswap-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-26-cyfrin-eulerswap-v2-0
title: Configured reserves may not guarantee protection against liquidation
vuln_class: []
---

# Configured reserves may not guarantee protection against liquidation

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-26-cyfrin-eulerswap-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-26-cyfrin-eulerswap-v2.0.md)_

---

**Description:** According to the [EulerSwap whitepaper](https://github.com/euler-xyz/euler-swap/blob/1022c0bb3c034d905005f4c5aee0932a66adf4f8/docs/whitepaper/EulerSwap_White_Paper.pdf):

> The space of possible reserves is determined by how much real liquidity an LP has and how much debt their operator is allowed to hold. Since EulerSwap AMMs do not always hold the assets used to service swaps at all times, they perform calculations based on virtual reserves and debt limits, rather than on strictly real reserves. Each EulerSwap LP can configure independent virtual reserve levels. These reserves define the maximum debt exposure an AMM will take on. Note that the effective LTV must always remain below the borrowing LTV of the lending vault to prevent liquidation.

This implies that, under proper configuration, an AMM should not be at risk of liquidation due to excessive loan-to-value (LTV). However, external factors can still undermine this guarantee.

For example, if another position in the same collateral vault is liquidated and leaves behind bad debt, the value of the shared collateral used for liquidity could drop. This would affect the effective LTV of all positions using that vault, including those managed by the EulerSwap AMM.

An attacker could exploit this situation by initiating a swap that pushes the AMM's position right up to the liquidation threshold, leveraging the degraded collateral value caused by unrelated bad debt.

**Recommended Mitigation:** Consider enforcing an explicit LTV check after each borrowing operation, and introduce a configurable maximum LTV parameter in `EulerSwapParams`. Additionally, clarify in the documentation that Euler account owners are responsible for monitoring the health of their vaults and should take proactive steps if the collateral accrues bad debt or drops in value—since this can happen independently of swap activity.

**Euler:** Acknowledged. Doing a health computation at the end of a swap would cost too much gas.

**Cyfrin:** The Euler team added several points in their documentation regarding liquidation concerns in [PR#93](https://github.com/euler-xyz/euler-swap/pull/93)

\clearpage

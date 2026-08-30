---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-1-7
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-02-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
tags:
- firm:cyfrin
- report:2024-02-23-cyfrin-swell-barracuda
title: Multiple attack paths to force `swETH::reprice` to revert by increasing or
  decreasing swETH total supply
vuln_class: []
---

# Multiple attack paths to force `swETH::reprice` to revert by increasing or decreasing swETH total supply

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-02-23-cyfrin-swell-barracuda.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md)_

---

**Description:** The current total swETH supply is [used](https://github.com/SwellNetwork/v3-contracts-lst/blob/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/swETH.sol#L268-L273) in `swETH::reprice` to enforce the maximum allowed total swETH supply difference during repricings. Total supply can decrease for 2 reasons:
1. [Withdrawal being finalized](https://github.com/SwellNetwork/v3-contracts-lst/blob/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/swEXIT.sol#L205)
2. User calls [`swETH::burn`](https://github.com/SwellNetwork/v3-contracts-lst/blob/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/swETH.sol#L350-L356) to burn their own swETH

Total supply can also increase by users calling `swETH::deposit`.

The closer the current supply difference is to the maximum tolerated difference percentage, the greater chance an attacker can front-run the repricing transaction causing it to revert by:
1. Depositing a large enough amount of ETH via `swETH::deposit` to increase total supply
2. Burning their own swETH to decrease total supply
3. Finalizing one or more withdrawals (users can finalize others withdrawals) to decrease total supply

**Recommended mitigation:**
Some possible mitigations include:
* Add a burner role and assigned it only to `swEXIT`, also add the corresponding modifier to check this role to `swETH::burn`
* Only allow the owner of an NFT to finalize their owned withdrawal requests

However these potential mitigations restrict functionality while still enabling an attacker to revert the reprice via the `swETH::deposit` route. Another option would be to have the bot perform the repricing transaction through a service such as [flashbots](https://www.flashbots.net/) such that the transaction can't be front-run; this would prevent all of the attack paths while still preserving the ability for users to burn their swETH and to finalize others withdrawals.

**Swell:** Using flashbots to perform repricing transactions.

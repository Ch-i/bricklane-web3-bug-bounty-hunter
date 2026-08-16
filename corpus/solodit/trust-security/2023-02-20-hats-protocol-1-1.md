---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-20-hats-protocol-1-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-02-20T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md
tags:
- firm:trust-security
- report:2023-02-20-hats-protocol
title: TRST-M-2 Attacker can DOS minting of new top hats in low-fee chains
vuln_class: []
---

# TRST-M-2 Attacker can DOS minting of new top hats in low-fee chains

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-02-20-Hats Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-20-Hats%20Protocol.md)_

---

**Description:**
In Hats protocol, anyone can be assigned a top hat via the `mintTopHat()` function. The top 
hats are structured with top 32 bits acting as a domain ID, and the lower 224 bits are 
cleared. There are therefore up to 2^32 = ~ 4 billion top hats. Once they are all consumed, 
`mintTopHat()` will always fail:
```solidity
          // uint32 lastTopHatId will overflow in brackets
             topHatId = uint256(++lastTopHatId) << 224;
```     
This behavior exposes the project to a DOS vector, where an attacker can mint 4 billion top 
hats in a loop and make the function unusable, forcing a redeploy of Hats protocol. This is 
unrealistic on ETH mainnet due to gas consumption, but definitely achievable on the 
cheaper L2 networks. As the project will be deployed on a large variety of EVM blockchains, 
this poses a significant risk.

**Recommended Mitigation:**
Require a non-refundable deposit fee (paid in native token) when minting a top hat. Price it 
so that consuming the 32-bit space will be impossible. This can also serve as a revenue 
stream for the Hats project.

**Team Response:**
Acknowledged; electing not to address in v1 for several reasons:
1. Additional requirement to set & manage authorization for withdrawal
2. Challenge of setting a consistently reasonable fee on chains without stablecoin based native tokens (i.e. all except for Gnosis Chain) / the added complexity and 
centralization risk of making the fee adjustable
3. Contract size constraints

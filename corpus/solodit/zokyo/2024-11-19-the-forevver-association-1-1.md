---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-11-19-the-forevver-association-1-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-11-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-19-The%20Forevver%20Association.md
tags:
- firm:zokyo
- report:2024-11-19-the-forevver-association
title: Lack of Event Emissions for Critical State Changes in Fias Token Contract
vuln_class: []
---

# Lack of Event Emissions for Critical State Changes in Fias Token Contract

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-11-19-The Forevver Association.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-11-19-The%20Forevver%20Association.md)_

---

**Severity** - Informational

**Status** - Acknowledged

**Description**:

The Fias token contract, including its V2 upgrade, fails to emit events for significant state changes, particularly during token minting in the initialize function and token burning in the burn function. 


**Recommendation**:


For the initialize function:
Define and emit a custom event for the initial token minting. For example:
event InitialMint(address indexed to, uint256 amount);

```solidity
function initialize() public initializer {
   __ERC20_init("Fias", "FIAS");
   _mint(LITCRAFT_MINTER, LITCRAFT_LIMIT*(10**18));
   emit InitialMint(LITCRAFT_MINTER, LITCRAFT_LIMIT*(10**18));
   _mint(FOREVVER_MINTER, FOREVVER_LIMIT*(10**18));
   emit InitialMint(FOREVVER_MINTER, FOREVVER_LIMIT*(10**18));
}
```
For the burn function:
Utilize OpenZeppelin's built-in _burn function, which already emits a Transfer event. If additional information is needed, consider adding a custom event:
event TokensBurned(address indexed burner, uint256 amount);

```solidity
function burn(uint256 amount) public {
   _burn(_msgSender(), amount);
   emit TokensBurned(_msgSender(), amount);
}
```

**Client comment**: 

this would be nice to add if we change anything and it’s odd that it isn’t part of the default OpenZeppelin functions, but there is no security risk to this.

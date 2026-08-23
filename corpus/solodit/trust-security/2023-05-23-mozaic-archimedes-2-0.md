---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-23-mozaic-archimedes-2-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-05-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md
tags:
- firm:trust-security
- report:2023-05-23-mozaic-archimedes
title: TRST-L-1 Theoretical reentrancy attack when TYPE_MINT_BURN proposals are executed
vuln_class: []
---

# TRST-L-1 Theoretical reentrancy attack when TYPE_MINT_BURN proposals are executed

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-05-23-Mozaic Archimedes.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md)_

---

**Description:**
The senate can pass a proposal to mint or burn tokens.
 ```solidity
        if(proposals[_proposalId].actionType == TYPE_MINT_BURN) {
            (address _token, address _to, uint256 _amount, bool _flag) = 
                abi.decode(proposals[_proposalId].payload, (address, address, uint256, bool));
        if(_flag) {
            IXMozToken(_token).mint(_amount, _to);
        } else {
                     IXMozToken(_token).burn(_amount, _to);
        }
        proposals[_proposalId].executed = true;
        }
```

Note that the proposal is only marked as executed at the end of execution, but execution is 
checked at the start of the function.

```solidity
        function execute(uint256 _proposalId) public onlyCouncil {
                 require(proposals[_proposalId].executed == false, "Error: 
            Proposal already executed.");
        require(proposals[_proposalId].confirmation >= threshold, "Error: Not enough confirmations.");
```

Interaction with tokens should generally be assumed to grant arbitrary call execution to users. 
If the mint or `burn()` calls call `execute()` again, the proposal will be executed twice, resulting in 
double the amount minted or burned. Specifically for XMoz, it is not anticipated to yield 
execution to the **to** address, so the threat remains theoretical.


**Recommended Mitigation:**
Follow the Check-Effects-Interactions design pattern, mark the function as executed at the 
start.

**Team Response:**
Fixed.

**Mitigation review:**
The `execute()` function is now protected with the **nonReentrant** modifier.

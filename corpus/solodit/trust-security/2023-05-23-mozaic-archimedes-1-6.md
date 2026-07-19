---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-23-mozaic-archimedes-1-6
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-05-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md
tags:
- firm:trust-security
- report:2023-05-23-mozaic-archimedes
title: TRST-M-7 MozToken allows owner to mint an arbitrary amount of tokens, although
  supply is fixed
vuln_class: []
---

# TRST-M-7 MozToken allows owner to mint an arbitrary amount of tokens, although supply is fixed

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-05-23-Mozaic Archimedes.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md)_

---

**Description:**
Supply of MozToken is defined to be fixed at 1B tokens:
**Max Supply**
1B MOZ will be minted at the genesis and will be the entire finite supply of tokens

However, there is an exposed `mint()` function which allows the owner to mint arbitrary 
amount of tokens.
```solidity
        function mint(address to, uint256 amount) public onlyOwner {
            _mint(to, amount);
            }
```
This would typically be in the centralization risks section, however due to the fact that the 
documentation is potentially misleading users, it must appear in the main report as well.

**Recommended mitigation:**
Remove the `mint()` function.

**Team response:**
Fixed.

**Mitigation review:**
The fix made only the staking contract capable of minting tokens.
```solidity
        function mint(uint256 _amount, address _to) external   onlyStakingContract {
            _mint(_to, _amount);
           }
```
However, the centralization issue remains as the owner can change the staking contract at 
once.
```solidity
        function setStakingContract(address _mozStaking) external onlyOwner {
              require(_mozStaking != address(0x0), "Invalid address");
             mozStaking = _mozStaking;
            }
```

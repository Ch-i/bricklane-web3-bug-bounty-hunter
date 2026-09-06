---
affected_contracts: []
derives_from: []
id: solodit-0x52-2024-09-22-stusdcxbloom-0-7
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-09-22T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md
tags:
- firm:0x52
- report:2024-09-22-stusdcxbloom
title: '[H-08] TBY#burn incorrectly burns id 0 for all burns causing complete loss
  of funds for lenders'
vuln_class: []
---

# [H-08] TBY#burn incorrectly burns id 0 for all burns causing complete loss of funds for lenders

_Section severity (from Solodit section header): High_  
_Audit firm: 0x52_  
_Source report: [2024-09-22-stUSDCxBloom.md](https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md)_

---

**Details**

[Tby.sol#L78-L82](https://github.com/Blueberryfi/bloom-v2/blob/87a60380331cc914be41ad57691f08b532a4d6fb/src/token/Tby.sol#L78-L82)

    function burn(uint256 id, address account, uint256 amount) external onlyBloom {
        _totalSupply[id] -= amount;
        _burn(account, 0, amount);
        emit Burn(account, id, amount);
    }

The burn function is misconfigured and will always attempt to burn id == 0 from the user. For the first round of tbys the burn function will work but after that it will result in all tbys being unredeemable and causing complete loss of funds to LPs.

**Lines of Code**

[Tby.sol#L78-L82](https://github.com/Blueberryfi/bloom-v2/blob/87a60380331cc914be41ad57691f08b532a4d6fb/src/token/Tby.sol#L78-L82)

**Recommendation**

\_burn should be correct to take id rather than 0 as the input

**Remediation**

Fixed as recommended in bloom-v2 [PR#13](https://github.com/Blueberryfi/bloom-v2/pull/13/)

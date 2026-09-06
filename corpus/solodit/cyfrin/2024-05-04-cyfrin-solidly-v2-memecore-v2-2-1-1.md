---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-04-cyfrin-solidly-v2-memecore-v2-2-1-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-05-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md
tags:
- firm:cyfrin
- report:2024-05-04-cyfrin-solidly-v2-memecore-v2-2
title: Consider a two-step ownership transfer
vuln_class: []
---

# Consider a two-step ownership transfer

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md)_

---

**Description:** In the `SolidtlyV2-memecore` contracts the owner is set as `msg.sender` in `SolidlyV2Factory` when deployed.

It can also be changed using `SolidlyV2Factory::setOwner`:
```solidity
    function setOwner(address _newOwner) external {
        require(msg.sender == owner);
        owner = _newOwner;
    }
```

Here there's a risk that the owner is lost if the new address not correct. This would result in some functionality not being available, like assigning new copilots and adjusting fees.

**Impact:** The `owner` can mistakenly be given to an account that is out of the protocol's control.

**Recommended Mitigation:** Consider implementing a two-step ownership transfer where `owner` first sets a `pendingOwner` then the `pendingOwner` can accept the new ownership , like OpenZeppelin [`Ownable2Step`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/access/Ownable2Step.sol)

**Solidly Labs:** Acknowledged.

**Cyfrin:** Acknowledged.

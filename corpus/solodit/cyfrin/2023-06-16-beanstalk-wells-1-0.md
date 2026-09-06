---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-16-beanstalk-wells-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-06-16T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md
tags:
- firm:cyfrin
- report:2023-06-16-beanstalk-wells
title: Should ensure uniqueness of the tokens of Wells
vuln_class: []
---

# Should ensure uniqueness of the tokens of Wells

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-16-Beanstalk wells.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md)_

---

**Description:** The current implementation does not enforce uniqueness in the tokens of Wells.
Anyone can call `Aquifer::boreWell()` with malicious `Well` implementation to set up a trap for victims.
Through communication with the protocol team, it is understood that all Wells are considered _guilty until proven innocent_.
But it is still desirable to verify the Well on `Aquifier::boreWell` and prevent deployments of malicious Wells.
It is also strongly recommended to prohibit changing `tokens()` after the deployment.

If a Well has duplicate tokens, an attack path shown below exists, and there can be more.

**Impact:** While we assume users will be warned explicitly about malicious Wells and not likely to interact with invalid Wells, we evaluate the severity to MEDIUM.

**Proof of Concept:** Let us say tokens[0]=tokens[1].
An honest LP calls `addLiquidity([1 ether,1 ether], 200 ether, address)`, and the reserves will be (1 ether, 1 ether). But anyone can call `skim()` and take `1 ether` out. This is because `skimAmounts` relies on the `balanceOf()`, which will return `2 ether` for the first loop.

```solidity
function skim(address recipient) external nonReentrant returns (uint[] memory skimAmounts) {
    IERC20[] memory _tokens = tokens();
    uint[] memory reserves = _getReserves(_tokens.length);
    skimAmounts = new uint[](_tokens.length);
    for (uint i; i < _tokens.length; ++i) {
        skimAmounts[i] = _tokens[i].balanceOf(address(this)) - reserves[i];
        if (skimAmounts[i] > 0) {
            _tokens[i].safeTransfer(recipient, skimAmounts[i]);
        }
    }
}
```

**Recommended Mitigation:**
- Do not allow changing the Well tokens once deployed.
- Require the uniqueness of the tokens during `boreWell()`.

**Beanstalk:** Fixed in commit [f10e05a](https://github.com/BeanstalkFarms/Basin/pull/81/commits/f10e05a32f60ec288ef6064e665cae797b800b39).

**Cyfrin:** Acknowledged.

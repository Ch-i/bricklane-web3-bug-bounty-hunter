---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-3-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: '`MembershipERC1155` implementation contract can be initialized'
vuln_class: []
---

# `MembershipERC1155` implementation contract can be initialized

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** `MembershipERC1155` is an implementation contract intended to be used with the Transparent upgradeable proxy pattern; however, it can be initialized since the `initialize()` function can be called by anyone.

**Impact:** This cannot be abused in any way other than initializing the implementation contract, which does not affect the proxy but may be confusing for consumers.

**Recommended Mitigation:** Consider invoking [`Initializable::_disableInitializers`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/72c152dc1c41f23d7c504e175f5b417fccc89426/contracts/proxy/utils/Initializable.sol#L184-L203) within the body of the constructor.

**One World Project:** Added in [`09b6f0f`](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/commit/09b6f0f978d2a8d2952a6938bf5756bec8a0170d).

**Cyfrin:** Verified. `_disabledInitializers()` is now called in the constructor.

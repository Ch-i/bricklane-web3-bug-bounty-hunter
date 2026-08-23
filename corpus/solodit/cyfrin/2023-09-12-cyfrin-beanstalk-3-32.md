---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-32
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Extra attention must be paid to future contract upgrades that utilize new or
  otherwise modify existing low-level calls
vuln_class: []
---

# Extra attention must be paid to future contract upgrades that utilize new or otherwise modify existing low-level calls

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

Care must be taken when introducing new features to Beanstalk that leverage low-level calls to ensure that they cannot be manipulated to appear as if those to functions that use `LibDiamond::enforceIsOwnerOrContract` originated from Beanstalk. This could allow a caller to circumvent this check, giving them access to privileged functions in the `UnripeFacet`, `PauseFacet`, `FundraiserFacet`, and `WhitelistFacet`.  While this does not appear to be immediately exploitable, it is important to understand that a successful exploit would require access to either an arbitrary external call within Beanstalk or a `delegateCall` in the context of Beanstalk following a low-level call in which the Beanstalk Diamond is the `msg.sender`. To reiterate, special attention must be paid to the implications of additions in any future upgrades that may introduce unsafe arbitrary external calls, especially considering usage with the `DepotFacet`, `FarmFacet`, `Pipeline`, and `LibETH`/`LibWETH`.

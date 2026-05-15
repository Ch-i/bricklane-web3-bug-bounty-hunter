---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-10
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: '`InitBip9` incorrectly references BIP-8 in the contract NatSpec'
vuln_class: []
---

# `InitBip9` incorrectly references BIP-8 in the contract NatSpec

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

The contract NatSpec for `InitBip9` currently incorrectly references BIP-8. This should be updated to avoid confusion:

```diff
    /**
     * @author Publius
-    * @title InitBip8 runs the code for BIP-8.
+    * @title InitBip9 runs the code for BIP-9.
    **/

contract InitBip9 {
```

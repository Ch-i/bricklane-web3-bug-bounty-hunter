---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-04-13-lukso-lsp-audit-2-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-04-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md
tags:
- firm:trust-security
- report:2023-04-13-lukso-lsp-audit
title: TRST-L-3 Relayer can choose amount of gas for delivery of message
vuln_class: []
---

# TRST-L-3 Relayer can choose amount of gas for delivery of message

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-04-13-LUKSO LSP audit.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-04-13-LUKSO%20LSP%20audit.md)_

---

**Description:**
LSP6 supports relaying of calls using a supplied signature. The encoded message is defined as:
 ```solidity
        bytes memory encodedMessage = abi.encodePacked( LSP6_VERSION,
           block.chainid,
              nonce,
                   msgValue,
         payload
     );
```
The message doesn't include a gas parameter, which means the relayer can specify any gas 
amount. If the provided gas is insufficient, the entire transaction will revert. However, if the called contract exhibits different behavior depending on the supplied gas, a relayer (attacker) 
has control over that behavior.

**Recommended Mitigation:**
Signed message should include the gas amount passed. Care should be taken to verify there 
is enough gas in the current state for the gas amount not to be truncated due to the 63/64 
rule.

**Team response:**
We decided not to implement this check as this would require the user to sign the gas limit 
provided to the call. This would affect the user experience with more complications. We 
decided to keep it as it is for now and implement the fix in the future if the problem is raised.

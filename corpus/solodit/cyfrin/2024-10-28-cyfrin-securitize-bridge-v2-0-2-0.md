---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-28-cyfrin-securitize-bridge-v2-0-2-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-10-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-28-cyfrin-securitize-bridge-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-28-cyfrin-securitize-bridge-v2-0
title: Add a validation to check the message sender and the token value
vuln_class: []
---

# Add a validation to check the message sender and the token value

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-28-cyfrin-securitize-bridge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-28-cyfrin-securitize-bridge-v2.0.md)_

---

**Description:** The `SecuritizeBridge` contract has a potential concern in its token bridging functionality.
While the contract is designed to work with compliance-verified investors, there's a gap in the validation process:

In the current Implementation:
- The contract checks if users have enough tokens to bridge (`balanceOf` check).
- It validates if tokens are not locked (`validateLockedTokens` check).
However, it doesn't explicitly verify if the sender is a valid investor.

As a result, when a user attempts to bridge 0 tokens, both validation checks will pass.
This means non-validated investors could successfully execute bridge transactions with 0 tokens.
While this doesn't result in any token transfer, it creates unnecessary cross-chain messages and potentially create noise in system monitoring and event logs

**Securitize:** Fixed in commit [6529fe](https://bitbucket.org/securitize_dev/bc-securitize-bridge-sc/commits/6529fe67789adab2266590f8581ef594e162aec5).

**Cyfrin:** Verified.


\clearpage

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-12-18T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-18-cyfrin-the-standard-auto-redemption-v2-0
title: Chainlink Functions HTTP request is missing authentication
vuln_class: []
---

# Chainlink Functions HTTP request is missing authentication

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md)_

---

**Description:** The `source` constant defined within `AutoRedemption` is used to execute the corresponding JavaScript code within the Chainlink Functions DON; however, the target API endpoint is exposed without any form of authentication which allows any observer to send requests.

**Impact:** A coordinated DDoS attack on the API endpoint could result in the server going down. This will cause requests to fail, meaning the Chainlink subscription will be billed but the auto redemption peg mechanism will not function as intended.

**Recommended Mitigation:** At a minimum, implement rate limiting. Preferably add authentication to the request using [Chainlink Functions secrets](https://docs.chain.link/chainlink-functions/resources/secrets).

**The Standard DAO:** Partially fixed by adding rate limiting to the API. Will also consider later adding an encrypted secret to the request.

**Cyfrin:** Acknowledged. Use of encrypted secrets is recommended.

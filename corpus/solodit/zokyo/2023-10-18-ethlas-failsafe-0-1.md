---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-10-18-ethlas-failsafe-0-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-10-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-10-18-Ethlas%20Failsafe.md
tags:
- firm:zokyo
- report:2023-10-18-ethlas-failsafe
title: Clickjacking Vulnerability in failsafe.eleoslabs.io
vuln_class: []
---

# Clickjacking Vulnerability in failsafe.eleoslabs.io

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-10-18-Ethlas Failsafe.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-10-18-Ethlas%20Failsafe.md)_

---

**Severity** : Low 

**Status**: Resolved 

**Description** :

 Clickjacking, also known as UI Redress Attack, is a malicious technique where an attacker tricks a user into clicking on something different from what the user perceives. In this case, a malicious actor can use an invisible or disguised iframe embedding https://failsafe.eleoslabs.io/ to mislead the users of the website into performing unintended actions without their knowledge.
an iframe is used to embed the failsafe.eleoslabs.io within another webpage, which can potentially allow an attacker to overlay other content or make the iframe transparent to deceive the user into interacting with the embedded page.
Impact: If successfully exploited, this vulnerability could lead to a range of impacts, including, but not limited to:
Unauthorized actions being performed on behalf of the user.
Loss of sensitive user data.
Damage to the reputation of the impacted site.

**Recommendation**: 

To mitigate this vulnerability, consider implementing the following measures:
Content Security Policy (CSP): Use the frame-ancestors directive to specify which websites are allowed to embed your site within iframes.


Content-Security-Policy: frame-ancestors 'none';
 This will prevent the page from being embedded within iframes, mitigating the Clickjacking risk.


X-Frame-Options Header: Employ the X-Frame-Options HTTP header on your website. This header can have values like DENY or SAMEORIGIN, which will block the page from being embedded in an iframe from other domains.

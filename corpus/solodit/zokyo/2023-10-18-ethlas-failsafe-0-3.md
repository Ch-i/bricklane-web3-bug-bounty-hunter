---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-10-18-ethlas-failsafe-0-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-10-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-10-18-Ethlas%20Failsafe.md
tags:
- firm:zokyo
- report:2023-10-18-ethlas-failsafe
title: Lack of Secure HTTP Headers
vuln_class: []
---

# Lack of Secure HTTP Headers

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-10-18-Ethlas Failsafe.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-10-18-Ethlas%20Failsafe.md)_

---

**Severity** : Low

**Status** : Resolved 



**Description**: 

Content Security Policy. Content Security Policy (CSP) was developed to allow an application developer to define the type and location of resources allowed to be loaded within the context of a given website.
Strict-Transport-Security. HTTP headers are well known and its implementation can make your application more secure. HTTP Strict Transport Security (HSTS) is a web security policy mechanism which helps to protect websites against protocol downgrade attacks and cookie hijacking. It allows web servers to declare that web browsers (or other complying user agents) should only interact with it using secure HTTPS connections, and never via the insecure HTTP protocol. HSTS is an IETF standards track protocol and is specified in RFC 6797. A server implements an HSTS policy by supplying a header (Strict-Transport-Security) over an HTTPS connection (HSTS headers over HTTP are ignored).
Problem Details
The web application does not use a set of industry-standard HTTP headers to  enhance security. The attacker can exploit the absence of these headers to  introduce vulnerabilities like Cross-Site Scripting and clickjacking attacks.
Affected Areas:
 https://failsafe.eleoslabs.io/ 


**Proof of Concept**

The following is needed in order to reproduce this issue:

Step 1 - Run the following command from the curl configured terminal and observe that the secure http headers are missing.
curl -I -X GET https://failsafe.eleoslabs.io/  --insecure
Recommendation
Implement the recommended HTTP security response headers based on need and application requirements. Set attributes and values as securely as possible based on application requirements.
Content-Security-Policy: Content Security Policy is an effective measure to protect your site from XSS attacks. By whitelisting sources of approved content, you can prevent the browser from loading malicious assets.
Referrer-Policy: Referrer Policy is a new header that allows a site to control how much information the browser includes with navigations away from a document and should be set by all sites.

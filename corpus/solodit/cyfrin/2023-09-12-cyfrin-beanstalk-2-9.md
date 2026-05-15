---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-2-9
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Incorrect formatting of `MetadataFacet::uri` JSON results in broken metadata
  which cannot be displayed by external clients
vuln_class: []
---

# Incorrect formatting of `MetadataFacet::uri` JSON results in broken metadata which cannot be displayed by external clients

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

**Description:** For fully on-chain metadata, external clients expect the URI of a token to contain a base64 encoded JSON object that contains the metadata and base64 encoded SVG image. Currently, [`MetadataFacet::uri`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/metadata/MetadataFacet.sol#L30-L51) is missing multiple quotations and commas within the encoded string which breaks its JSON formatting.

**Impact:** External clients such as OpenSea are currently unable to display Beanstalk token metadata due to broken JSON formatting.

**Recommended Mitigation:** Add missing quotation marks and commas. Ensure the resulting encoded bytes are that of valid JSON.

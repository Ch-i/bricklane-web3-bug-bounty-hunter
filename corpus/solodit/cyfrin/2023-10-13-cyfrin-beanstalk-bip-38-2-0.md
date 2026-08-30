---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-10-13-cyfrin-beanstalk-bip-38-2-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-10-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-10-13-cyfrin-beanstalk-bip-38.md
tags:
- firm:cyfrin
- report:2023-10-13-cyfrin-beanstalk-bip-38
title: Incorrect handling of metadata traits in the attributes of `MetadataFacet::uri`
vuln_class: []
---

# Incorrect handling of metadata traits in the attributes of `MetadataFacet::uri`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-10-13-cyfrin-beanstalk-bip-38.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-10-13-cyfrin-beanstalk-bip-38.md)_

---

**Description:** For fully on-chain metadata, external clients expect the URI of a token to contain a base64 encoded JSON object that contains the metadata and base64 encoded SVG image. As raised previously, if these attributes are intented to be utilized as metadata traits then failure to correctly handle the packed encoding of the [attributes variable](https://github.com/BeanstalkFarms/Beanstalk/blob/12c608a22535e3a1fe379db1153185fe43851ea7/protocol/contracts/beanstalk/metadata/MetadataFacet.sol#L38-L47) as an array of JSON objects in `MetadataFacet::uri` results in non-standard JSON metadata when subsequently [returned](https://github.com/BeanstalkFarms/Beanstalk/blob/12c608a22535e3a1fe379db1153185fe43851ea7/protocol/contracts/beanstalk/metadata/MetadataFacet.sol#L48-L55), meaning it cannot be fully utilized by external clients.

**Impact:** External clients such as OpenSea are currently unable to display Beanstalk token metadata traits due to non-standard JSON formatting.

**Recommended Mitigation:** Refactor the inline metadata attributes as an array of metadata trait objects, ensuring the resulting encoded bytes are that of valid JSON.

**Beanstalk Farms:** Fixed in commit [47fef03](https://github.com/BeanstalkFarms/Beanstalk/pull/655/commits/47fef03a37527c839acd4696db08fbf0bbcd5a71).

**Cyfrin:** Acknowledged.


\clearpage

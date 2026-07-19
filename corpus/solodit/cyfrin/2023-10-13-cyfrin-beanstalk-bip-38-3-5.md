---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-10-13-cyfrin-beanstalk-bip-38-3-5
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-10-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-10-13-cyfrin-beanstalk-bip-38.md
tags:
- firm:cyfrin
- report:2023-10-13-cyfrin-beanstalk-bip-38
title: Consider moving the `MetadataFacet::uri` disclaimer from metadata attributes
  to the description
vuln_class: []
---

# Consider moving the `MetadataFacet::uri` disclaimer from metadata attributes to the description

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-10-13-cyfrin-beanstalk-bip-38.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-10-13-cyfrin-beanstalk-bip-38.md)_

---

The [disclaimer](https://github.com/BeanstalkFarms/Beanstalk/blob/12c608a22535e3a1fe379db1153185fe43851ea7/protocol/contracts/beanstalk/metadata/MetadataFacet.sol#L46) within `MetadataFacet::uri` currently resides at the end of the JSON attributes; however, this may be better placed within the metadata description instead.

**Beanstalk Farms:** The disclaimer placement was largely inspired by [Uniswap V3’s NFT](https://opensea.io/assets/ethereum/0xc36442b4a4522e871399cd717abdd847ab11fe88/528320) and thus, feel that the attribute section is an adequate place to keep it.

**Cyfrin:** Acknowledged.

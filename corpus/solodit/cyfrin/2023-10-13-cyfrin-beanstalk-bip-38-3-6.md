---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-10-13-cyfrin-beanstalk-bip-38-3-6
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-10-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-10-13-cyfrin-beanstalk-bip-38.md
tags:
- firm:cyfrin
- report:2023-10-13-cyfrin-beanstalk-bip-38
title: Incorrect comment in `MetadataImage::sciNotation` should be corrected
vuln_class: []
---

# Incorrect comment in `MetadataImage::sciNotation` should be corrected

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-10-13-cyfrin-beanstalk-bip-38.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-10-13-cyfrin-beanstalk-bip-38.md)_

---

`MetadataImage::sciNotation` is intended to convert an input Stem to its string representation, using scientific notation if the value is [greater than 1e5](https://github.com/BeanstalkFarms/Beanstalk/blob/12c608a22535e3a1fe379db1153185fe43851ea7/protocol/contracts/beanstalk/metadata/MetadataImage.sol#L539). Related comments [referencing 1e7](https://github.com/BeanstalkFarms/Beanstalk/blob/12c608a22535e3a1fe379db1153185fe43851ea7/protocol/contracts/beanstalk/metadata/MetadataImage.sol#L538) as the threshold are incorrect and so should be modified to 1e5.

**Beanstalk Farms:** Fixed in commit [81e452e](https://github.com/BeanstalkFarms/Beanstalk/commit/81e452e41c2533dfc49543dc70fba15ed3c6cc2f).

**Cyfrin:** Acknowledged.

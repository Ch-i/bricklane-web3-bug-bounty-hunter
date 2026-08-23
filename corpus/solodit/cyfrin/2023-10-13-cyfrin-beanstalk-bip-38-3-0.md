---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-10-13-cyfrin-beanstalk-bip-38-3-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-10-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-10-13-cyfrin-beanstalk-bip-38.md
tags:
- firm:cyfrin
- report:2023-10-13-cyfrin-beanstalk-bip-38
title: Resetting of `withdrawSeasons` state was not executed on-chain as part of the
  BIP-36 upgrade
vuln_class: []
---

# Resetting of `withdrawSeasons` state was not executed on-chain as part of the BIP-36 upgrade

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-10-13-cyfrin-beanstalk-bip-38.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-10-13-cyfrin-beanstalk-bip-38.md)_

---

The [addition](https://github.com/BeanstalkFarms/Beanstalk/blob/12c608a22535e3a1fe379db1153185fe43851ea7/protocol/contracts/beanstalk/init/InitBipNewSilo.sol#L42-L43) of `s.season.withdrawSeasons = 0` to `InitBipNewSilo::init` does not appear to have been present in the [version](https://etherscan.io/address/0xf6c77e64473b913101f0ec1bfb75a386aba15b9e#code) executed as part of the BIP-36 upgrade. Therefore, to have the state of Beanstalk accurately reflect this change, another upgrade should be performed to have this logic executed on-chain.

**Beanstalk Farms:** Fixed in commit [cca6250](https://github.com/BeanstalkFarms/Beanstalk/pull/655/commits/cca625052179764c930be707a68a43952ec54ddf).

**Cyfrin:** Acknowledged.

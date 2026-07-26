---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-31
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Inaccurate NatSpec comments in `AppStorage`
vuln_class: []
---

# Inaccurate NatSpec comments in `AppStorage`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

Within the [`AppStorage::SiloSettings`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/AppStorage.sol#L373) struct, there is a [comment](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/AppStorage.sol#L381-L385) that references the use of a `delegatecall` to calculate the Bean Denominated Value (BDV) of a token. This is incorrect – it is a [`staticcall`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Silo/LibTokenSilo.sol#L287) to the selector corresponding to any of the signatures contained within [`BDVFacet`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/silo/BDVFacet.sol#L18) and not [`tokenToBdv`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/AppStorage.sol#L368C18-L368C28).

Other inaccuracies are present in both the [`AppStorage::AppStorage`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/AppStorage.sol#L441-L550) and [`AppStorage::State`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/AppStorage.sol#L86-L160) structs where there are members missing from the documentation and/or documented in an order that is not reflective of the subsequent declarations. These should be checked carefully and updated accordingly for the sake of consistency and minimizing confusion.

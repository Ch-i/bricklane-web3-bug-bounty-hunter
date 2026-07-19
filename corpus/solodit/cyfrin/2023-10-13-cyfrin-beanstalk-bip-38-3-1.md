---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-10-13-cyfrin-beanstalk-bip-38-3-1
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
title: Changes to initialization contracts are not recommended after they are executed
  on-chain
vuln_class: []
---

# Changes to initialization contracts are not recommended after they are executed on-chain

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-10-13-cyfrin-beanstalk-bip-38.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-10-13-cyfrin-beanstalk-bip-38.md)_

---

It is understood that certain modifications to BIP initialization contracts have been made retroactively with the intention that, if run again, any new deployments of the Beanstalk protocol by replaying this history will reflect the current state of Beanstalk. One particular [modification](https://github.com/BeanstalkFarms/Beanstalk/blob/12c608a22535e3a1fe379db1153185fe43851ea7/protocol/contracts/beanstalk/init/InitDiamond.sol#L62) to `InitDiamond::init`, setting the `stemStartSeason` to zero, while seemingly benign as migration logic in `LibSilo` appears to be bypassed, would result in underdlow within `LibLegacyTokenSilo::_calcGrownStalkForDeposit` when calculating the [Season diff](https://github.com/BeanstalkFarms/Beanstalk/blob/12c608a22535e3a1fe379db1153185fe43851ea7/protocol/contracts/libraries/Silo/LibLegacyTokenSilo.sol#L469). This issue will be present until `InitBipNewSilo::init` excutes, setting the `stemStartSeason` state to the [Season in which it is executed](https://github.com/BeanstalkFarms/Beanstalk/blob/12c608a22535e3a1fe379db1153185fe43851ea7/protocol/contracts/beanstalk/init/InitBipNewSilo.sol#L76-L77). It is therefore recommended that initialization scripts are ossified after being executed on-chain to maintain an accurate history of the protocol: its mechanism developments, bugs and related upgrades/mitigations.

**Beanstalk Farms:** The purpose of such changes is to future proof future deployments of Beanstalk. If someone were to deploy a fresh Beanstalk, it is important that the protocol continues to function as expected with all upgrades already implemented.

The expectation is that a new Beanstalk would be initialized only with `InitDiamond` and that Beanstalk would automatically be on the newest version. The other `Init` contracts are intended strictly to migrate from a previous version to the next.

The `LibLegacyTokenSilo` is only used to provide legacy support and migration functionality for Silo V2. This includes, the `MigrationFacet`, `LegacyClaimWithdrawalFacet` and `seasonToStem(address token, uint32 season)` in `SiloExit`. The expectation is that a new Beanstalk would be deployed immediately with the Silo V3 upgrade and thus have no reason to be backwards compatable with Silo V2 or support migration from V2 to V3 in any capacity.

**Cyfrin:** Acknowledged.

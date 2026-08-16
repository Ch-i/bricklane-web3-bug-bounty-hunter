---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-10-13-cyfrin-beanstalk-bip-38-3-2
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
title: Lack of slippage protection when removing liquidity from BEAN:3CRV MetaPool
  and adding liquidity to BEAN:ETH Well could result in loss of funds due to sandwich
  attack
vuln_class: []
---

# Lack of slippage protection when removing liquidity from BEAN:3CRV MetaPool and adding liquidity to BEAN:ETH Well could result in loss of funds due to sandwich attack

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-10-13-cyfrin-beanstalk-bip-38.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-10-13-cyfrin-beanstalk-bip-38.md)_

---

Currently, the second and third steps of the *Migration Process*, as provided in BIP-38 specification, are not included in the scope of this BIP. The primary risk associated with these steps is the swap of BEAN:3CRV LP Tokens for BEAN:ETH Well LP Tokens, given the size of the swap to be performed. Sandwiching of the transaction that executes this swap could result in loss of funds. Therefore, the use of reasonable slippage parameters is essential to prevent this. It is understood that the current use of zero [slippage parameters](https://github.com/BeanstalkFarms/Beanstalk/blob/12c608a22535e3a1fe379db1153185fe43851ea7/protocol/scripts/beanEthMigration.js#L26) within the `beanEthMigration.js` migration script when removing liquidity from the MetaPool and [adding liquidity](https://github.com/BeanstalkFarms/Beanstalk/blob/12c608a22535e3a1fe379db1153185fe43851ea7/protocol/scripts/beanEthMigration.js#L39) to the Well is only intended for testing purposes. The swap path from 3CRV -> WETH will either be executed manually via the BCM on a DEX aggregator with MEV protection or via an OTC swap, and the BCM will ensure the proper use of slippage parameters when removing/adding liquidity. It is essential that this is the case.

**Beanstalk Farms:** This script is only expected to be used to mock the migration to aid in testing. The expectation is that it will never be used to execute code on mainnet and thus no slippage parameter is added.

**Cyfrin:** Acknowledged.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-2-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Lack of existence validation when adding a new unripe token
vuln_class: []
---

# Lack of existence validation when adding a new unripe token

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

**Description:** [`UnripeFacet::addUnripeToken`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/barn/UnripeFacet.sol#L227-L236) does not currently check if the `unripeToken` has been already added. Unlike `LibWhitelist::whitelistToken`, which has [this check](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Silo/LibWhitelist.sol#L80), the current implementation allows the Beanstalk Community Multisig (BCM) to modify the settings for existing unripe tokens.

**Impact:** Unripe tokens were introduced as a mechanism for recapitalization after the governance hack of April 2022. While the BCM affords more flexibility and control compared to the previous implementation of fully on-chain governance, if the BCM were to become compromised in any way or sign off on a vulnerable contract upgrade, privileged access to this function could result in the ability to manipulate the unripe token mechanisms that exist within the protocol by altering the Merkle root for a pre-existing unripe token.

**Recommended Mitigation:** Validate that the unripe token has not already been added to prevent changes to existing unripe tokens.

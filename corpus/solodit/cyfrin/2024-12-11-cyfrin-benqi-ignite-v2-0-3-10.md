---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-3-10
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-12-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-11-cyfrin-benqi-ignite-v2-0
title: Typo in `Ignite::registerWithPrevalidatedQiStake` NatSpec
vuln_class: []
---

# Typo in `Ignite::registerWithPrevalidatedQiStake` NatSpec

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** There is a typo in the `Ignite::registerWithPrevalidatedQiStake` [NatSpec](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L355).

**Recommended Mitigation:**
```diff
  /**
   * @notice Register a new node with a prevalidated QI deposit amount
-  * @param  beneficiary User no whose behalf the registration is made
+  * @param  beneficiary User on whose behalf the registration is made
   * @param  nodeId Node ID of the validator
   * @param  blsProofOfPossession BLS proof of possession (public key + signature)
   * @param  validationDuration Duration of the validation in seconds
   * @param  qiAmount The amount of QI that was staked
  */
```

**BENQI:** Fixed in commit [50c7c1a](https://github.com/Benqi-fi/ignite-contracts/pull/16/commits/50c7c1a81cbe7058116e53d178f61f828993ebc9).

**Cyfrin:** Verified.

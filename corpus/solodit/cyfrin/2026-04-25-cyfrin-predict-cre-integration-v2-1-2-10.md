---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-25-cyfrin-predict-cre-integration-v2-1-2-10
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-04-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-25-cyfrin-predict-cre-integration-v2-1
title: Missing deploy-time input validation in constructor and initializer
vuln_class: []
---

# Missing deploy-time input validation in constructor and initializer

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-25-cyfrin-predict-cre-integration-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md)_

---

**Description:** Grouping of deploy-time defensive-depth gaps where constructor or initializer inputs are stored or consumed without a sanity check. Both members are Informational per the Gate 2 deploy-time exception - a bad value produces an obviously-broken state the operator can recover from by redeployment, but in each case the contract offers no defensive reject-on-bad-input that would convert an operator mistake into a clean revert instead of silent dysfunction.

---

**1. `ChainlinkAdapter` constructor missing zero-address validation on `_verifierProxy` and `_ctf`**

`ChainlinkAdapter` constructor assigns both `_verifierProxy` and `_ctf` as immutable without zero-address checks. Deploy-time misconfiguration is irrecoverable because the fields are immutable.

```solidity
40:    constructor(address _forwarderAddress, address _verifierProxy, address _ctf) ChainlinkReceiverBase(_forwarderAddress) {
45:        VERIFIER_PROXY = IVerifierProxy(_verifierProxy);
46:        CTF = IConditionalTokens(_ctf);
47:    }
```

**Impact:** Zero-address footgun at deploy; irrecoverable because fields are immutable.

**Recommended:**

```solidity
if (_verifierProxy == address(0)) revert ChainlinkAdapter__InvalidVerifierProxy();
if (_ctf == address(0)) revert ChainlinkAdapter__InvalidCTF();
```

---

**2. `ChainlinkUpDownAdapter::_initialize` lacks lower-bound sanity check on `startTimestamp`**

`_initialize` enforces only `startTimestamp < block.timestamp`. There is no lower bound - any timestamp in the past is accepted, from five minutes ago to twenty-five years ago. The expected operational flow is that `initialize` is called with a `startTimestamp` within the last interval; an operator mistake (stale script, stale variable, copy-paste from prior deployment) could pass a deep-past `startTimestamp` without the contract noticing.

**Impact:** If `startTimestamp` is sufficiently far in the past, the contract pre-creates rounds whose `endTimestamps` are also in the past. Because `CTF.prepareCondition` has no tradability gate and the Data Streams historical API serves observations at those timestamps, every pre-created round has a deterministic outcome that any public observer of `RoundSeriesInitialized` can recover and trade on. Severity is Informational because only `INITIALIZER_ROLE` can call `initialize` - this is defensive-depth against operator mistakes rather than an unprivileged exploit.

Source: `ChainlinkUpDownAdapter.sol:377-379`.

**Recommended:**

```solidity
if (block.timestamp - startTimestamp > interval * 2) {
    revert ChainlinkUpDownAdapter__StartTimestampTooOld();
}
```

The threshold should be tight enough to reject stale values but loose enough to tolerate reasonable propagation and scheduling windows.

---

**Predict.fun:** Acknowledged, the initializer will be a multi-sig so it takes time to gather all the signature, worst case they just redeploy.

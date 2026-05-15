---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-kleidi-report-0-23
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-kleidi-report
title: '[L-24] Original Hot Signer that becomes Compromised or Malicious can take
  over all undeployed systems'
vuln_class: []
---

# [L-24] Original Hot Signer that becomes Compromised or Malicious can take over all undeployed systems

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Kleidi_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md)_

---

**Impact**

The known issues specify:

https://github.com/solidity-labs-io/kleidi/blob/1a06ac16bc99d0b4081281329d03064c3737f5e4/docs/KNOWN_ISSUES.md#L5

```markdown
- if the hot signers are malicious or compromised, they can deploy a compromised system instance on a new chain with compromised recovery spells and malicious calldata checks that allow funds to be stolen
```

This is correct, however, it's worth highlighting that malicious / compromised hot signers may be removed from a live deployment

However, because of the logic used to deploy the system on new networks, the previously removed hot signer would still be able to deploy and compromise the system

**Proof Of Concept**

- Setup system as intended on Chain A
- Do not deploy on Chain B
- Hot Signer N key gets leaked
- Remove Hot Signer N from Chain A
- Hot Signer N can deploy on Chain B and compromise it

Meaning that the risk of compromised Hot Signers doesn't end once a Hot Signer is removed from the original chain, but only if they are removed from all chains

**Mitigation**

Users should:
- Deploy all instances they want to secure
- Remove all hot signers from all deployed chains
- Setup each chain at the time in which that's necessary

It may also be best to enforce that one of the owners is setting up a deployment on any other chain, however this shares a similar risk that if they are compromised they could still compromised other chains

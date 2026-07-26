---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-kleidi-report-0-24
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-kleidi-report
title: '[L-25] Docs Typos'
vuln_class: []
---

# [L-25] Docs Typos

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Kleidi_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md)_

---

**Merge marks**

https://github.com/solidity-labs-io/kleidi/blob/1a06ac16bc99d0b4081281329d03064c3737f5e4/docs/TESTING.md#L53-L59

```markdown
so that when there is a further sanity check failure by a mutant the spec can be marked as violated.
<<<<<<< HEAD
>>>>>>> 81590cd (remove redundant spec)
=======
>>>>>>> 0cf1c3c (remove redundant spec)
>>>>>>> 664c0e1 (remove redundant spec)
=======
```

**Pseudocode doesn't exist**

https://github.com/solidity-labs-io/kleidi/blob/1a06ac16bc99d0b4081281329d03064c3737f5e4/docs/CALLDATA_WHITELISTING.md#L34-L45

```markdown
This means that to supply to any market, the same function is called with different calldata parameters. This is where the array of calldata checks is used.

```solidity
    struct Index {
        uint16 startIndex;
        uint16 endIndex;
        EnumerableSet.Bytes32Set dataHashes;
    }

    contract address => bytes4 function selector => Index[] calldataChecks;
```


**Broken Link**

https://github.com/solidity-labs-io/kleidi/blob/1a06ac16bc99d0b4081281329d03064c3737f5e4/README.md#L7

```markdown
- **Security**: The protocol is designed by the world class Smart Contract engineering team at Solidity Labs. It has had components formally verified, and has been audited twice with no critical or high issues discovered. It is designed to be used with Gnosis Safe multisigs, which are battle-tested and have secured tens of billions of dollars in assets. See our internal audit log [here](docs/security/AUDIT_LOG.md).
```

**Mitigation**
Should be /docs/AUDIT_LOG.md

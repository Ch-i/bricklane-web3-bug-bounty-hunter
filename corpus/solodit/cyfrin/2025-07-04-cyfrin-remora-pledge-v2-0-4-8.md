---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-4-8
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: In `RemoraToken::transfer`, `transferFrom` and `_exchangeAllowed` perform all
  checks for each user together in order to prevent unnecessary work
vuln_class: []
---

# In `RemoraToken::transfer`, `transferFrom` and `_exchangeAllowed` perform all checks for each user together in order to prevent unnecessary work

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** In `RemoraToken::transfer`, `transferFrom` and `_exchangeAllowed` perform all checks for each user together in order to prevent unnecessary work.

`transfer`:
```solidity
        bool fromWL = _whitelist[sender];
        if (!fromWL) _unlockTokens(sender, value, false);

        bool toWL = _whitelist[to];
        if (!toWL) _lockTokens(to, value);
```

`transferFrom`:
```solidity
        bool fromWL = _whitelist[from];
        if (!fromWL) _unlockTokens(from, value, false);

        bool toWL = _whitelist[to];
        if (!toWL) _lockTokens(to, value);
```

`_exchangeAllowed`:
```solidity
        (bool resFrom, ) = hasSignedDocs(from);
        if (!resFrom && !_whitelist[from]) revert TermsAndConditionsNotSigned(from);

        (bool resTo, ) = hasSignedDocs(to);
        if (!resTo && !_whitelist[to]) revert TermsAndConditionsNotSigned(to);
```

**Remora:** Fixed in commit [59cf2eb](https://github.com/remora-projects/remora-smart-contracts/commit/59cf2eb26742de48988623fdd029d17b2993ba2f).

**Cyfrin:** Verified.

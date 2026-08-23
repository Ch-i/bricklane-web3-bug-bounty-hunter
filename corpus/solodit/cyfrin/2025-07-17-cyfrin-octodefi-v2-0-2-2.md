---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-2-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-07-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-17-cyfrin-octodefi-v2-0
title: DoS of automation due to potential zero value transfer reverts
vuln_class: []
---

# DoS of automation due to potential zero value transfer reverts

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-17-cyfrin-octodefi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md)_

---

**Description:** Token burn percentages specified by `primaryTokenBurn` and `tokenBurn` are simply restricted to the range `(0, 100]`. If the burn percentage is configured to 100%, this can result in scenarios where the burn amount in `FeeHandler.handleFee()` returned by `_feeCalculation()` is non-zero while the total fee to be distributed between the beneficiary/creator/vault is zero. While the standard OpenZeppelin ERC-20 implementation does not revert on zero value transfers, and it is unlikely that the burn percentages will be set that high anyway, it is possible and so is advisable to skip transfers in this case if any of the distribution amounts is zero to avoid DoS for token implementations that do revert on zero value transfers.

**Impact:** Automation can revert when attempting to make payment if the burn percentage is configured as 100%.

**Recommended Mitigation:** Similar to the validation on `burnAmount`, only attempt to perform token transfers if the respective beneficiary/creator/vault amounts are non-zero.

**OctoDeFi:** Fixed by PR [\#14](https://github.com/octodefi/strategy-builder-plugin/pull/14). Due to the introduced pull-based method from M-3, this issue has also been resolved, as no tokens are transferred directly anymore.

**Cyfrin:** Verified. The push transfer pattern has been updated to a pull pattern that resolves this issue.

\clearpage

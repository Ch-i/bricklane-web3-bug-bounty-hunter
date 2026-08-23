---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-3-11
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Remove empty function `BTCY::_checkMinSharesAfterWithdraw`
vuln_class: []
---

# Remove empty function `BTCY::_checkMinSharesAfterWithdraw`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** Remove empty function `BTCY::_checkMinSharesAfterWithdraw` since it is never used; just add its comments inside `_withdraw`:
```diff
    function _withdraw(address _caller, address _receiver, address _owner, uint256 _assets, uint256 _shares)
        internal
        override
        whenNotPaused
    {
        // snip: unrelated code

        // Transfer fee to fee recipient if fee > 0
        if (fee > 0) {
            address recipient = feeRecipient();
            require(recipient != address(0), FeeRecipientNotSet());
            IERC20(asset()).safeTransfer(recipient, fee);
        }

-       _checkMinSharesAfterWithdraw();
+       // only enforce MIN_SHARES on deposits to stop donation attacks. Skipping the
+       // check here avoids griefing via tiny front‑run deposits that would otherwise
+       // make legitimate withdrawals revert when total supply dips below MIN_SHARES.
    }
```

**Aarc:** Fixed in commit [8f7015e](https://github.com/aarc-xyz/btcy-contracts-main/commit/8f7015e4a9134ecda73c56c17f4e223446134a9f).

**Cyfrin:** Verified.

\clearpage

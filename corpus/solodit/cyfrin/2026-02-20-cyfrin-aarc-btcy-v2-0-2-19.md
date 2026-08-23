---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-2-19
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: '`BTCY::_checkMinShares` should not allow zero `totalSupply` as it is called
  after deposits'
vuln_class: []
---

# `BTCY::_checkMinShares` should not allow zero `totalSupply` as it is called after deposits

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** Per finding _"ERC4626::deposit,redeem,mint,withdraw should revert if they would return zero"_, vaults can be manipulated via "stealth donations" where small amounts are deposited to the vault which increase the vault's tokens but not the shares.

The current implementation of `BTCY::_checkMinShares` allows this since it allows `totalSupply == 0`, however since this function is only ever called after a deposit, it shouldn't allow this:

```diff
    function _checkMinShares() internal view {
-       uint256 _totalSupply = totalSupply();
-       require(_totalSupply == 0 || _totalSupply >= MIN_SHARES, MinSharesViolation());
+       require(totalSupply() >= MIN_SHARES, MinSharesViolation());
    }
```

Additionally consider removing this function and just enforcing the check inside `BTCY::_deposit`:
```diff
    function _deposit(address _caller, address _receiver, uint256 _assets, uint256 _shares)
        internal
        override
        whenNotPaused
    {
        super._deposit(_caller, _receiver, _assets, _shares);
-       _checkMinShares();
+       require(totalSupply() >= MIN_SHARES, MinSharesViolation());
    }
```

**Aarc:** Fixed in commit [a982611](https://github.com/aarc-xyz/btcy-contracts-main/commit/a98261155c698fb1b3ef013ddc509e244d39377f).

**Cyfrin:** Verified.

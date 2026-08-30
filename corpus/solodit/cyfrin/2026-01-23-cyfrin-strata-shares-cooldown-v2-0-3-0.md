---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-23-cyfrin-strata-shares-cooldown-v2-0-3-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-01-23T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-23-cyfrin-strata-shares-cooldown-v2-0
title: Skip call to `CDO::accrueFee` when there are no fees to charge
vuln_class: []
---

# Skip call to `CDO::accrueFee` when there are no fees to charge

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md)_

---

**Description:** During a withdrawal/redemption, when the `TExitMode` is != than `SharesLock`, `CDO::accrueFees` is called to charge any fees that may have to be paid for the withdrawal, but there are multiple cases when no fees are charged (i.e., when finalizing a withdrawal from the `SharesCooldown`.
```solidity
    function _withdraw(
        ...
    ) internal virtual {
       ...

        if (exitMode == IStrataCDO.TExitMode.SharesLock) {
            ...
        }

        uint256 baseAssetsGross = convertToAssets(sharesGross);
        uint256 fee = Math.saturatingSub(baseAssetsGross, baseAssets);

        _burn(owner, sharesGross);
//@audit => No need to call cdo.accrueFee when no fees will be charged
@>      cdo.accrueFee(address(this), fee);
        ...
    }

```


**Recommended Mitigation:** In the scenarios where no fees will be charged, it is not necessary to call `CDO::accrueFees`.

**Strata:** Fixed in commit [b690dcd](https://github.com/Strata-Money/contracts-tranches/commit/b690dcde46a41553ac5d44810367e7c222bc6082).

**Cyfrin:** Verified.

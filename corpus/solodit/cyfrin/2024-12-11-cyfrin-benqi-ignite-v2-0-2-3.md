---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-2-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-12-11T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-11-cyfrin-benqi-ignite-v2-0
title: '`StakingContract::slippage` can be outside of `minSlippage` or `maxSlippage`'
vuln_class: []
---

# `StakingContract::slippage` can be outside of `minSlippage` or `maxSlippage`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** When the BENQI admin sets the `slippage` state by calling [`StakingContract::setSlippage`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L313-328), it is validated that this new value is between the `minSlippage` and `maxSlippage` thresholds:

```solidity
require(
    _slippage >= minSlippage && _slippage <= maxSlippage,
    "Slippage must be between min and max"
);
```

The admin can also change both `minSlippage` and `maxSlippage` via [`StakingContract::setMinSlippage`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L330-345) and [`StakingContract::setMaxSlippage`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L347-360); however, neither of these functions has any validation that the `slippage` state variable remains within the boundaries.

**Impact:** Incorrect usage of either `StakingContract::setMaxSlippage` or `StakingContract::setMinSlippage` can result in the `slippage` state variable being outside the range.

**Proof of Concept:** The following test can be added to `stakingContract.test.js` under `describe("setSlippage")`:

```javascript
it("can have slippage outside of max and min", async function () {
    // slippage is set to 4
    await stakingContract.connect(benqiAdmin).setSlippage(4);
    // max slippage is updated below it
    await stakingContract.connect(benqiAdmin).setMaxSlippage(3);

    const slippage = await stakingContract.slippage();
    const maxSlippage = await stakingContract.maxSlippage();
    expect(slippage).to.be.greaterThan(maxSlippage);
});
```

**Recommended Mitigation:** Consider validating that the `slippage` state variable is within the boundaries set using `setMin/MaxSlippage()`.

**BENQI:** Fixed in commits [96e1b96](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/commit/96e1b9610970259cffdf44fd7cf1af527016b0ce) and [dbb13c5](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/commit/dbb13c55047e4ce52e39f833196fc78ed5c0cf8a).

**Cyfrin:** Verified.

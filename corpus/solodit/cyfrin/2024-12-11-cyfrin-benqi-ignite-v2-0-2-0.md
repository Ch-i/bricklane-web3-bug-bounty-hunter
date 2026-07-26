---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-2-0
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
title: '`StakingContract` refunds are affected by global parameter updates'
vuln_class: []
---

# `StakingContract` refunds are affected by global parameter updates

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** When [`StakingContract::refundStakedAmount`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L691-741) is called by the BENQI admin, the following validation is performed using the globally-defined `refundPeriod`:

```solidity
require(
    block.timestamp > record.timestamp + refundPeriod,
    "Refund period not reached"
);
```

The [`StakingContract::StakeRecord`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L69-77) struct does not have a corresponding member and so does not store the value of `refundPeriod` at the time of staking; however, if [`StakingContract::setRefundPeriod`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L675-689) is called with an updated period then that of an existing record could be shorter/longer than expected.

**Impact:** The refund period for existing records could be affected by global parameter updates.

**Recommended Mitigation:** Consider adding an additional member to the `StakeRecord` struct to store the value of `refundPeriod` at the time of staking.

**BENQI:** Acknowledged, working as expected.

**Cyfrin:** Acknowledged.

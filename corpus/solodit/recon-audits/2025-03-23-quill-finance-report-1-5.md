---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-quill-finance-report-1-5
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-quill-finance-report
title: '[L-06] Zombie Trove Spam Risk when Oracle is Highly Predictable could be used
  to borrow at lower rate and never get redeemed'
vuln_class: []
---

# [L-06] Zombie Trove Spam Risk when Oracle is Highly Predictable could be used to borrow at lower rate and never get redeemed

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Quill_Finance_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md)_

---

**Impact**

The logic for Redemptions looks as follows:

The trove data is loaded from the storage pointer

https://github.com/subvisual/quill/blob/d4a5dcc168dfc315eef6a4c9c465a36c86ca0ddc/contracts/src/TroveManager.sol#L821-L829

```solidity
        SingleRedemptionValues memory singleRedemption;
        // Let’s check if there’s a pending zombie trove from previous redemption
        if (lastZombieTroveId != 0) {
            singleRedemption.troveId = lastZombieTroveId;
            singleRedemption.isZombieTrove = true;
        } else {
            singleRedemption.troveId = sortedTrovesCached.getLast();
        }
        address lastBatchUpdatedInterest = address(0);
```

Then we loop, and a specific edge case could happen:

https://github.com/subvisual/quill/blob/d4a5dcc168dfc315eef6a4c9c465a36c86ca0ddc/contracts/src/TroveManager.sol#L843-L849

```solidity
            // Skip if ICR < 100%, to make sure that redemptions don’t decrease the CR of hit Troves
            if (getCurrentICR(singleRedemption.troveId, _price) < _100pct) {
                singleRedemption.troveId = nextUserToCheck;
                singleRedemption.isZombieTrove = false;
                continue;
            }

```

When the current trove is liquidatable, even if it's a zombie trove, it will be skipped

This is a necessity because technically the Trove cannot repay 100% of it's debt since it's underwater
And a liquidation is possible

However, this means that if we redeem another trove and make it a zombie, we are going to make the system forget about this one

The key pre-requisite is that each "forgotten" zombie trove must be underwater when this happens

Meaning that to pull this off reliably we'd need to find a highly volatile collateral feed and be able to perform these operations without getting the "Hidden Zombie" liquidated

This also requires the price to go down and then up "forever" hence it's low likelihood

However, introducing an oracle like Pyth, where deviations could be pushed each second could make this more likely

**Proof Of Concept**

**If you could use Pyth or smth, and have the Trove not liquidated you could create a ton of small troves and not pay the borrow rate**


Since the invariant is:
- Check zombie trove
- Skip if underwater

You could spam this to create a ton of zombie troves

The likelihood to pull this off on Mainnet is very low

The likelihood to pull this off with Pull or Manipulatable Oracle is a lot higher as you may be able to send different prices to the oracle


**Mitigation**

Ensure you monitor this behaviour and have liquidators available

Ultimately the R/R to pull this off is not great, so I doubt it will be attempted unless you introduce a Price Feed with Critical Vulnerabilities

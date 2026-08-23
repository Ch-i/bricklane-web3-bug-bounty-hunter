---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-1-6
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-bridgex-v2-0
title: No way to recover or refund unused eligible releases in the bridges
vuln_class: []
---

# No way to recover or refund unused eligible releases in the bridges

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** In the bridge contracts, users prepay the release fee via `Bridge::payReleaseFee` and receive a credit in `eligibleBridgeReleases[msg.sender]`. That credit is only consumed when pending releases are actually processed in  `Bridge::_processPendingReleases`.

There is no function or flow that allows users to recover, refund, or transfer unused eligibility. If a user pays for more releases than they have pending the extra eligibility remains in the contract forever and cannot be turned back into value or given to someone else. Eligibility is only decremented when a pending release is processed (and incremented again only when that single release fails):
```solidity
        for (uint i = 0; i < releases.length && eligibleBridgeReleases[recipient] > 0; i++) {
            if (releases[i].exists) {
                eligibleBridgeReleases[recipient]--;

                if (_releaseTokens(
                    releases[i].recipient,
                    releases[i].amount,
                    releases[i].destinationChain
                )) {
                    emit PendingReleaseProcessed(
                        releases[i].recipient,
                        releases[i].amount,
                        releases[i].sourceChainTxHash
                    );
                    releases[i].exists = false;
                } else {
                    eligibleBridgeReleases[recipient]++;
                    break;
                }
```
There is no other code path that decreases or refunds `eligibleBridgeReleases` for unused slots.

**Impact:** Users who overpay or never get pending releases end up with unused eligibility that cannot be refunded, transferred, or otherwise used.

**Recommended Mitigation:** Add a function (e.g. `refundUnusedEligibility` or `refundEligibleReleases(uint256 count)`) that lets users surrender unused `eligibleBridgeReleases` to have their remaining fees refunded.

**BridgeX:**
Acknowledged; a user's unused credits are consumed on future releases and refunds are impossible since fees are paid to relayers immediately. Adding a refund path would require the contract to hold funds introducing extra complexity and potential drain vectors.

\clearpage

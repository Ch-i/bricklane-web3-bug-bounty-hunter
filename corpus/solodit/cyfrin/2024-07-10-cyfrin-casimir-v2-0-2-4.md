---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-2-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-07-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-10-cyfrin-casimir-v2-0
title: Incorrect test setup leads to false test outcomes
vuln_class: []
---

# Incorrect test setup leads to false test outcomes

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-10-cyfrin-casimir-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md)_

---

**Description:** `IntegrationTest.t.sol` includes an integrated test that verifies the entire staking lifecycle. However, the current test setup, in several places, advances the blocks using foundry's `vm.roll` but neglects to adjust the timestamp using `vm.warp`.

This allows the test setup to claim rewards without any time delay.

_IntegrationTest.t.sol Line 151_
```solidity
>       vm.roll(block.number + eigenWithdrawals.withdrawalDelayBlocks() + 1); //@audit changing block without changing timestamp
        vm.prank(reporterAddress);
>       manager.claimRewards(); //@audit claiming at the same timestamp

        // Reporter runs after the heartbeat duration
        vm.warp(block.timestamp + 24 hours);
        timeMachine.setProofGenStartTime(0.5 hours);
        beaconChain.setNextTimestamp(timeMachine.proofGenStartTime());
        vm.startPrank(reporterAddress);
        manager.startReport();
        manager.syncValidators(abi.encode(beaconChain.getActiveBalanceSum(), 0));
        manager.finalizeReport();
        vm.stopPrank();
````

Moving blocks without updating the timestamp is an unrealistic simulation of the blockchain. As of EigenLayer M2, `WithdrawDelayBlocks` are 50400, which is approximately 7 days. By advancing 50400 blocks without changing the timestamp, tests overlook several accounting edge cases related to delayed rewards. This is especially true because each reporting period lasts for 24 hours - this means there are 7 reporting periods before a pending reward can actually be claimed.

**Impact:** An incorrect setup can provide false assurance to the protocol that all edge cases are covered.

**Recommended Mitigation:** Consider modifying the test setup as follows:

- Run reports without instantly claiming rewards. This accurately reflects events on the real blockchain.
- Consider adjusting time whenever blocks are advanced.

**Casimir:**
Fixed in [290d8e1](https://github.com/casimirlabs/casimir-contracts/commit/290d8e11846c5d20ed6a059e32864c8227fb582d)

**Cyfrin:** Verified.

\clearpage

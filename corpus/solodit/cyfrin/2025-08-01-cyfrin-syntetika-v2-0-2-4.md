---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-2-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Unbounded `depositAddresses` can cause `CompliantDepositRegistry::challengeLatestBatch`
  to revert due to out of gas
vuln_class: []
---

# Unbounded `depositAddresses` can cause `CompliantDepositRegistry::challengeLatestBatch` to revert due to out of gas

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** `CompliantDepositRegistry::challengeLatestBatch` contains an unbounded loop that removes deposit addresses from the latest batch by calling `depositAddresses.pop()` repeatedly. When a large batch of deposit addresses is added via `CompliantDepositRegistry::addDepositAddresses`, challenging this batch could consume excessive gas, potentially exceeding the block gas limit and causing the transaction to revert. This creates a Denial of Service (DoS) vulnerability where legitimate challenges cannot be executed.

```solidity
function challengeLatestBatch() public onlyRole(CANCELER_ROLE) {
        require(latestBatchUnlockTime >= block.timestamp, NoChallengeAfterUnlock());

        uint256 _finalizedAddressesLength = finalizedAddressesLength;
        // Get rid of the challenged batch by removing it from the list
        uint256 batchLength = depositAddresses.length - _finalizedAddressesLength;
        for (uint256 i; i < batchLength; i++) {
            depositAddresses.pop();
        }<---------

        // Reset the challenge period to allow a new batch to be generated
        latestBatchUnlockTime = block.timestamp;

        emit BatchChallenged(_finalizedAddressesLength, block.timestamp, batchLength);
    }

```

**Impact:** Large batches become unchallengeable, allowing malicious or incorrect deposit addresses to be finalized.

**Proof of Concept:** **Recommended Mitigation:**
Implement limits on the amount of addresses that can be added through  `CompliantDepositRegistry::addDepositAddresses`.

**Syntetika:**
Fixed in commit [319e7ea](https://github.com/SyntetikaLabs/monorepo/commit/319e7ead926e9973e1257337893c031522506bab) by changing `challengeLatestBatch` to allow cancelling in batches.

**Cyfrin:** Verified.

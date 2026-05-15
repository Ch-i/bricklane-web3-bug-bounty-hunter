---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-4-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Cache storage to prevent identical storage reads
vuln_class: []
---

# Cache storage to prevent identical storage reads

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** Reading from storage is expensive; cache storage to prevent identical storage reads:
* `ComplianceChecker.sol`:
```solidity
// cache `for` loop storage lengths in `isCompliant`
59:            optionIndex < _complianceOptions.length;
66:                sbtIndex < _complianceOptions[optionIndex].requiredSBTs.length;
```

* `CompliantDepositRegistry.sol`:
```solidity
// cache `investorDepositMap[investor]` in `getDepositAddress`
60:        require(investorDepositMap[investor] > 0, UnregisteredInvestor());
64:        return depositAddresses[investorDepositMap[investor]];

// cache `nextDepositAddressIndex` in `registerDepositAddress`
93:                nextDepositAddressIndex < depositAddresses.length &&
102:        investorDepositMap[msg.sender] = nextDepositAddressIndex;

// cache `getDepositAddress(msg.sender)` in `registerDepositAddress`
// ideally do this by using a named return variable, assigning straight to it,
// using the named return variable to emit the event then deleting the obsolete
// `return` statement
104:        emit DepositAddressSet(msg.sender, getDepositAddress(msg.sender));
106:        return getDepositAddress(msg.sender);

// cache `depositAddresses.length` in `getDepositAddresses`
128:        if (startIndex + count > depositAddresses.length) {
129:            returnLength = depositAddresses.length - startIndex;
134:            i < count && startIndex + i < depositAddresses.length;

// cache `depositAddresses.length` in `addDepositAddresses`
// just invert the order of these two statements then use `startIndex`
// to set `finalizedAddressesLength`
154:        finalizedAddressesLength = depositAddresses.length;
156:        uint startIndex = depositAddresses.length;

// cache `block.timestamp + batchChallengePeriod` in `addDepositAddresses`
// and use it to set `latestBatchUnlockTime` and also to emit the event
161:        latestBatchUnlockTime = block.timestamp + batchChallengePeriod;
165:            latestBatchUnlockTime,

// cache `finalizedAddressesLength` and use `block.timestamp` instead of
// `latestBatchUnlockTime` when emitting event in `challengeLatestBatch`
199:        uint batchLength = depositAddresses.length - finalizedAddressesLength;
208:            finalizedAddressesLength,
209:            latestBatchUnlockTime,
```

* `Blacklistable.sol`:
```solidity
// use input `_newBlacklister` when emitting event in `updateBlackLister`
74:        emit BlacklisterChanged(blacklister);
```

* `Minter.sol`:
```solidity
// cache `custodian` in `transferToCustody`
135:        baseAsset.safeTransfer(custodian, amount);
136:        emit FundsTransferredToCustody(amount, custodian);
```

* `StakingVault.sol`:
```solidity
// cache `cooldownDuration` in `redeem, withdraw`
137:        if (cooldownDuration == 0) {
142:            cooldownDuration;
159:        if (cooldownDuration == 0) {
164:            cooldownDuration;

// use input `duration` when emitting event in `setCooldownDuration`
220:        cooldownDuration = duration;
221:        emit CooldownDurationUpdated(previousDuration, cooldownDuration);

// cache `lastDistributionTimestamp` in `getUnvestedAmount` if first `return`
// statement is unlikely to be frequently triggered
271:        if (lastDistributionTimestamp > block.timestamp) {
275:            lastDistributionTimestamp;
```

**Syntetika:**
Fixed in commits [bc24502](https://github.com/SyntetikaLabs/monorepo/commit/bc245024d7a3d4773661a2eb82284653bfa7f46b), [8560039](https://github.com/SyntetikaLabs/monorepo/commit/8560039b80334a3ad234f7f90ff0a55e50d13edd), [bfad835](https://github.com/SyntetikaLabs/monorepo/commit/bfad8350a4b6b843c47bea023237271c198bfa84).

**Cyfrin:** Verified though ideally `StakingVault::withdraw` would also [cache](https://github.com/SyntetikaLabs/monorepo/blob/audit/issuance/src/vault/StakingVault.sol#L190-L195) `cooldownDuration` similar to the fix made inside `redeem`.

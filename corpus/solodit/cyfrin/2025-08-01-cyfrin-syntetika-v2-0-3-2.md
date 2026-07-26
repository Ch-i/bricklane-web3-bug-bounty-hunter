---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-3-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Prefer explicit `uint` sizes
vuln_class: []
---

# Prefer explicit `uint` sizes

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** Prefer explicit `uint` sizes:
* `Issuance`
```solidity
interfaces/minter/IBridgeMinter.sol
14:        uint id,
29:        uint id;

interfaces/galactica/IVerificationSBT.sol
45:        uint _expirationTime,
55:        uint _expirationTime

interfaces/token/IMintableERC20.sol
7:    function mint(address to, uint amount) external;
8:    function burn(address from, uint amount) external;

vault/StakingVault.sol
143:        uint assetsRedeemed = _redeemTo(shares, address(tokensHolder));
289:    ) internal returns (uint shares) {
306:    ) internal returns (uint assets) {
```

* `Deposit-Registry`:
```solidity
interfaces/ICompliantDepositRegistry.sol
44:        uint indexed startIndex,
45:        uint challengePeriodEnd,
48:    event BatchChallengePeriodSet(uint newChallengePeriod);
50:        uint indexed startIndex,
51:        uint challengePeriodEnd,
52:        uint batchLength
100:        uint startIndex,
101:        uint count
116:    function setBatchChallengePeriod(uint newChallengePeriod) external;

ComplianceChecker.sol
44:        for (uint i = 0; i < complianceOptions.length; i++) {
58:            uint optionIndex = 0;
65:                uint sbtIndex = 0;

CompliantDepositRegistry.sol
27:    uint public nextDepositAddressIndex;
30:    uint public batchChallengePeriod;
32:    uint public latestBatchUnlockTime;
34:    uint public finalizedAddressesLength;
44:        // Block the first deposit address so that the default uint does not point to a valid address
124:        uint startIndex,
125:        uint count
127:        uint returnLength = count;
133:            uint i = 0;
156:        uint startIndex = depositAddresses.length;
157:        for (uint i = 0; i < newDepositAddresses.length; i++) {
174:    function _setBatchChallengePeriod(uint newChallengePeriod) internal {
184:        uint newChallengePeriod
199:        uint batchLength = depositAddresses.length - finalizedAddressesLength;
200:        for (uint i = 0; i < batchLength; i++) {
```

**Syntetika:**
Fixed in commit [cb00843](https://github.com/SyntetikaLabs/monorepo/commit/cb0084368c85c4878dfd0af0fbca1c4924a36497).

**Cyfrin:** Verified.

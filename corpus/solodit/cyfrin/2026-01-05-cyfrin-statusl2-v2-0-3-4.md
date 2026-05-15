---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-3-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: New users can't be registered after slashing contrary to documentation
vuln_class: []
---

# New users can't be registered after slashing contrary to documentation

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** `RLN.sol` has variable `SET_SIZE`, which defines maximum number of registered users. During slashing, users are deleted from registry:
```solidity
    function slash(bytes32 privateKey, address rewardRecipient) private onlyRole(SLASHER_ROLE) {
        // Hash the private key using Poseidon to get identityCommitment
        uint256 identityCommitment = poseidonHasher.hash(uint256(privateKey));

        User memory member = members[identityCommitment];
        if (member.userAddress == address(0)) {
            revert RLN__MemberNotFound();
        }
        karma.slash(member.userAddress, rewardRecipient);
@>      delete members[identityCommitment];
    }
```
According to documentation https://github.com/status-im/status-network-monorepo/blob/develop/status-network-contracts/docs/rln.md#registry-capacity:
>Once the registry reaches capacity, new registrations are rejected until space is available. When accounts are slashed, their identity commitments are removed from the registry, freeing up space for new registrations.

However slashing accounts doesn't free up space for new registrations:
```solidity
    function register(uint256 identityCommitment, address user) external onlyRole(REGISTER_ROLE) {
@>      uint256 index = identityCommitmentIndex;
@>      if (index >= SET_SIZE) {
            revert RLN__SetIsFull();
        }
        if (members[identityCommitment].userAddress != address(0)) {
            revert RLN__IdCommitmentAlreadyRegistered();
        }

        /// forge-lint: disable-next-line(named-struct-fields)
        members[identityCommitment] = User(user, index);
        emit MemberRegistered(identityCommitment, index);

        unchecked {
@>          identityCommitmentIndex = index + 1;
        }
    }
```

**Impact:** New users can't be registered after slashing contrary to documentation.

**Recommended Mitigation:** Add missing feature or update documentation.

**StatusL2:** Fixed in [2c73d4d](https://github.com/status-im/status-network-monorepo/commit/2c73d4d6a597983e5170c6d1779e49100eed90f6).

**Cyfrin:** Verified.

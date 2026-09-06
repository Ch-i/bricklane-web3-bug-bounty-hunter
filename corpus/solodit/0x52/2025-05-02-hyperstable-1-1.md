---
affected_contracts: []
derives_from: []
id: solodit-0x52-2025-05-02-hyperstable-1-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-05-02T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2025-05-02-Hyperstable.md
tags:
- firm:0x52
- report:2025-05-02-hyperstable
title: '[M-02] Airdrop supply methodology has been changed leading to excess token
  emissions'
vuln_class: []
---

# [M-02] Airdrop supply methodology has been changed leading to excess token emissions

_Section severity (from Solodit section header): Medium_  
_Audit firm: 0x52_  
_Source report: [2025-05-02-Hyperstable.md](https://github.com/solodit/solodit_content/blob/main/reports/0x52/2025-05-02-Hyperstable.md)_

---

**Details**

[MerkleClaim.sol#L48-L69](https://github.com/velodrome-finance/v1/blob/de6b2a19b5174013112ad41f07cf98352bfe1f24/contracts/redeem/MerkleClaim.sol#L48-L69)

        function claim(
            address to,
            uint256 amount,
            bytes32[] calldata proof
        ) external {
            // Throw if address has already claimed tokens
            require(!hasClaimed[to], "ALREADY_CLAIMED");

            // Verify merkle proof, or revert if not in tree
            bytes32 leaf = keccak256(abi.encodePacked(to, amount));
            bool isValidLeaf = MerkleProof.verify(proof, merkleRoot, leaf);
            require(isValidLeaf, "NOT_IN_MERKLE");

            // Set address to claimed
            hasClaimed[to] = true;

            // Claim tokens for address
    @>      require(VELO.claim(to, amount), "CLAIM_FAILED");

            // Emit claim event
            emit Claim(to, amount);
        }

Above is the original `VELO` `MerkleClaim` code. Observe that when claiming, `VELO` is minted on demand. This is contrasted with `PegAirdrop` (`MerkleClaim` fork) which holds all the tokens and simply distributes them as users claim.

[EmissionScheduler.sol#L63-L80](https://github.com/hyperstable/contracts/blob/35db5f2d3c8c1adac30758357fbbcfe55f0144a3/src/governance/EmissionScheduler.sol#L63-L80)

        function epochEmission(uint256 _pegSupply, uint256 _veSupply) external returns (uint256, uint256, uint256) {
            uint256 currentEpoch = _currentEpoch();

            if (currentEpoch == lastEpoch) {
                return (0, 0, 0);
            }

            lastEpoch = currentEpoch;

    @>      uint256 toEmit = (_pegSupply - _veSupply).mulDiv(2, EMISSION_PRECISION);

            lastEpochEmission = toEmit;

            uint256 rebase = _calculateRebase(toEmit, _pegSupply, _veSupply);
            uint256 teamEmission = _calculateTeamEmission(toEmit, rebase);

            return (toEmit, rebase, teamEmission);
        }

This difference is quite important as `epochEmission` is based on the float percentage of `supply`. As a result these tokens which are undistributed will be incorrectly counted against the floating token `supply`. This will lead to excess token emissions until the claim period is over governance is able to recover them.

**Lines of Code**

[EmissionScheduler.sol#L72](https://github.com/hyperstable/contracts/blob/35db5f2d3c8c1adac30758357fbbcfe55f0144a3/src/governance/EmissionScheduler.sol#L72)

**Recommendation**

Consider removing the balance of `PegAirdrop` from the emission calculation or using an on-demand minting strategy similar to `VELO`.

**Remediation**

Fixed in [85be083](https://github.com/hyperstable/contracts/commit/85be083579af51f7c04b39233d8daab96bb40ff1). Distribution has been changed to on-demand minting.

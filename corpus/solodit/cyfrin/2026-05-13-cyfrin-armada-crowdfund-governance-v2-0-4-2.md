---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-4-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: State variable and struct field packing across `ArmadaCrowdfund`, `ArmadaGovernor`,
  `ArmadaToken`, `ShieldPauseController`
vuln_class: []
---

# State variable and struct field packing across `ArmadaCrowdfund`, `ArmadaGovernor`, `ArmadaToken`, `ShieldPauseController`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** Solidity lays state variables and struct fields out in declaration order; sub-32-byte types (`bool`, `address`, `uintN`<256, enum) only share a slot when declared adjacent. Placing a full-slot type between small fields forces each small field into its own slot. Reordering to group small fields together packs them - no type changes, no semantic change.

| Site | Location | Fix | Slots saved |
|---|---|---|---|
| `ArmadaCrowdfund` state | `ArmadaCrowdfund.sol:62, 94-102` | Group `phase` + 2×uint8 + 2×bool into one slot (5 bytes) | 1 |
| `ShieldPauseController` state | `ShieldPauseController.sol:40-55` | Group 4×bool + address into one slot (24 bytes) | 4 |
| `ArmadaToken` state | `ArmadaToken.sol:23-44` | Group 5×bool + address ahead of the mappings (25 bytes) | 4 |
| `ArmadaGovernor` state | `ArmadaGovernor.sol:145, 188-190` | Group 3×bool + address into one slot (23 bytes) | 2 |
| `HopConfig` struct | `IArmadaCrowdfund.sol:19` | Move `uint256 capUsdc` to end; pack the 3 small fields | 1 × 3 instances = 3 |
| `Participant` struct | `IArmadaCrowdfund.sol:26` | Move `uint256 committed` to end; pack `invitedBy` + 2×uint16 + bool | 1 × ~1,500 nodes (DESIGN NOTE `ArmadaCrowdfund.sol:825`) |
| `Proposal` struct | `ArmadaGovernor.sol:93` | Move the 4 bools up to pack with `proposer` + `proposalType` | 1 × every proposal |

**Impact:** ~20k gas per eliminated slot on first write, ~2.1k per cold SLOAD. Hot paths that read/write multiple packed fields together collapse into a single warm slot access: `finalize` / `claimRefund` (phase + refundMode), `_escrowCommit` / `_iterateCappedDemand` / `claim` (Participant fields), `_initProposal` / `castVote` / `queue` / `execute` / `cancel` (proposer + bools).

The `Participant` reorder dominates the aggregate win because it multiplies by the ~1,500 whitelisted `(addr, hop)` node cap - roughly 1,500 slots and ~30M gas of first-write cost amortized across the sale's lifetime.

Contracts are pre-mainnet, so reorders are safe on fresh deployment. `ArmadaGovernor` deploys via `ERC1967Proxy` - its contract-level and `Proposal` struct reorders must land before the first mainnet deployment, after which they break upgrade safety.

**Recommended Mitigation:** Contract-level reorders (types and visibility preserved):

```solidity
// ArmadaCrowdfund - 5 bytes packed
Phase public phase;
uint8 public launchTeamHop1Used;
uint8 public launchTeamHop2Used;
bool  public armLoaded;
bool  public refundMode;
```

```solidity
// ShieldPauseController - 24 bytes packed
bool    private _paused;
bool    public  windDownActive;
bool    public  windDownContractSet;
bool    public  windDownPauseUsed;
address public  windDownContract;
```

```solidity
// ArmadaToken - 25 bytes packed (declare ahead of the mappings)
bool    public transferable;
bool    public whitelistInitialized;
bool    public noDelegationSet;
bool    public authorizedDelegatorsInitialized;
bool    public windDownContractSet;
address public windDownContract;
```

```solidity
// ArmadaGovernor - 23 bytes packed
bool    public excludedAddressesLocked;
bool    public windDownActive;
bool    public windDownContractSet;
address public windDownContract;
```

Struct reorders:

```solidity
// HopConfig - slot 0: 5 bytes packed | slot 1: capUsdc
struct HopConfig {
    uint16  ceilingBps;
    uint8   maxInvites;
    uint16  maxInvitesReceived;
    uint256 capUsdc;
}

// Participant - slot 0: 25 bytes packed | slot 1: committed
struct Participant {
    address invitedBy;
    uint16  invitesReceived;
    uint16  invitesSent;
    bool    isWhitelisted;
    uint256 committed;
}

// Proposal - the 4 bools moved up to pack into slot 1 with proposer + proposalType (25 bytes)
struct Proposal {
    uint256 id;
    address proposer;
    ProposalType proposalType;
    bool    executed;
    bool    canceled;
    bool    queued;
    bool    vetoRatificationDenied;
    uint256 voteStart;
    uint256 voteEnd;
    uint256 executionDelay;
    uint256 snapshotBlock;
    uint256 snapshotEligibleSupply;
    uint256 snapshotQuorumBps;
    uint256 forVotes;
    uint256 againstVotes;
    uint256 abstainVotes;
    address[] targets;
    uint256[] values;
    bytes[]   calldatas;
    string    description;
}
```

**Armada:** Fixed in commit [d8e38dd](https://github.com/ship-armada/armada-poc/commit/d8e38ddd96cb1a49e590d027ca966105069f5d5b).

**Cyfrin:** Verified.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-02-cyfrin-stakelink-vesting-v2-0-2-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-08-02T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-02-cyfrin-stakelink-vesting-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-02-cyfrin-stakelink-vesting-v2-0
title: Storage variable layout can be optimized
vuln_class: []
---

# Storage variable layout can be optimized

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-02-cyfrin-stakelink-vesting-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-02-cyfrin-stakelink-vesting-v2.0.md)_

---

**Description:** The current storage layout uses 4 slots.

```solidity
    // maximum lock time in years
    uint256 public constant MAX_LOCK_TIME = 4;

    // address of SDL token
    IERC677 public immutable sdlToken;
    // address of SDL pool
    ISDLPool public immutable sdlPool;

    // whether vesting has been terminated
    bool public vestingTerminated;

    // amount of tokens claimed by the beneficiary
    uint256 public released;
    // address to receive vested SDL
    address public immutable beneficiary;
    // start time of vesting in seconds
    uint64 public immutable start;
    // duration of vesting in seconds
    uint64 public immutable duration;

    // lock time in years to use for staking vested SDL
    uint64 public lockTime;
    // list of reSDL token ids for each lock time
    uint256[] private reSDLTokenIds;
```
```
╭-------------------+-----------+------+--------+-------+---------------------------------------------╮
| Name              | Type      | Slot | Offset | Bytes | Contract                                    |
+=====================================================================================================+
| _owner            | address   | 0    | 0      | 20    | contracts/vesting/SDLVesting.sol:SDLVesting |
|-------------------+-----------+------+--------+-------+---------------------------------------------|
| vestingTerminated | bool      | 0    | 20     | 1     | contracts/vesting/SDLVesting.sol:SDLVesting |
|-------------------+-----------+------+--------+-------+---------------------------------------------|
| released          | uint256   | 1    | 0      | 32    | contracts/vesting/SDLVesting.sol:SDLVesting |
|-------------------+-----------+------+--------+-------+---------------------------------------------|
| lockTime          | uint64    | 2    | 0      | 8     | contracts/vesting/SDLVesting.sol:SDLVesting |
|-------------------+-----------+------+--------+-------+---------------------------------------------|
| reSDLTokenIds     | uint256[] | 3    | 0      | 32    | contracts/vesting/SDLVesting.sol:SDLVesting |
╰-------------------+-----------+------+--------+-------+---------------------------------------------╯
```
By moving the `lockTime` after `vestingTerminated ` we can reduce it to 3 slots:

```
╭-------------------+-----------+------+--------+-------+---------------------------------------------╮
| Name              | Type      | Slot | Offset | Bytes | Contract                                    |
+=====================================================================================================+
| _owner            | address   | 0    | 0      | 20    | contracts/vesting/SDLVesting.sol:SDLVesting |
|-------------------+-----------+------+--------+-------+---------------------------------------------|
| vestingTerminated | bool      | 0    | 20     | 1     | contracts/vesting/SDLVesting.sol:SDLVesting |
|-------------------+-----------+------+--------+-------+---------------------------------------------|
| lockTime          | uint64    | 0    | 21     | 8     | contracts/vesting/SDLVesting.sol:SDLVesting |
|-------------------+-----------+------+--------+-------+---------------------------------------------|
| released          | uint256   | 1    | 0      | 32    | contracts/vesting/SDLVesting.sol:SDLVesting |
|-------------------+-----------+------+--------+-------+---------------------------------------------|
| reSDLTokenIds     | uint256[] | 2    | 0      | 32    | contracts/vesting/SDLVesting.sol:SDLVesting |
╰-------------------+-----------+------+--------+-------+---------------------------------------------╯
```

```diff
    // maximum lock time in years
    uint256 public constant MAX_LOCK_TIME = 4;

    // address of SDL token
    IERC677 public immutable sdlToken;
    // address of SDL pool
    ISDLPool public immutable sdlPool;

    // whether vesting has been terminated
    bool public vestingTerminated;

+   // lock time in years to use for staking vested SDL
+   uint64 public lockTime;

    // amount of tokens claimed by the beneficiary
    uint256 public released;
    // address to receive vested SDL
    address public immutable beneficiary;
    // start time of vesting in seconds
    uint64 public immutable start;
    // duration of vesting in seconds
    uint64 public immutable duration;

-   // lock time in years to use for staking vested SDL
-   uint64 public lockTime;
    // list of reSDL token ids for each lock time
    uint256[] private reSDLTokenIds;
```


**Stake.Link:** Acknowledged.

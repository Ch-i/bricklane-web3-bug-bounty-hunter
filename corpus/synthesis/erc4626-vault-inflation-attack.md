---
id: synthesis-erc4626-vault-inflation-attack
source: synthesis
source_url: null
title: "ERC4626 vault inflation attack: pattern, variants, audit checklist"
ingested_at: 2026-05-15T00:00:00Z
vuln_class:
  - inflation-attack
  - donation-attack
  - first-depositor
  - rounding
  - share-price-manipulation
protocol_category:
  - vault
  - lending
  - yield
tags:
  - synthesis
  - erc4626
  - inflation-attack
  - donation
  - first-depositor
  - empty-market
derives_from:
  - rekt-resupplyfi-rekt
  - rekt-onyx-protocol-rekt
  - rekt-hundred-rekt2
  - rekt-radiant-capital-rekt
  - solodit-trust-security-2023-05-29-stella-0-3
  - solodit-trust-security-2023-05-28-orbital-finance-0-1
  - solodit-zokyo-2024-05-15-steadefi-0-0
  - solodit-zokyo-2024-01-24-narwhal-finance-2-0
  - solodit-zokyo-2024-03-06-vaultka-0-0
  - solodit-zokyo-2023-04-19-umami-0-1
  - solodit-zokyo-2023-08-30-vaultka-0-1
  - solodit-zokyo-2024-10-29-liberty-finance-0-0
  - solodit-zokyo-2023-06-09-narwhal-finance-0-0
  - solodit-cyfrin-2023-09-19-cyfrin-stakepet-0-1
  - solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-5
  - solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-1-1
  - solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-1-0
  - solodit-cyfrin-2025-12-19-cyfrin-lido-earn-v2-0-0-2
  - solodit-cyfrin-2025-12-19-cyfrin-lido-earn-v2-0-1-5
  - solodit-pashov-audit-group-2023-06-01-protectorate-1-1
  - solodit-pashov-audit-group-2022-11-01-yield-ninja-0-1
  - solodit-0x52-2023-12-18-ubet-0-0
  - solodit-hexens-2024-01-12-persistence-0-2
---

# ERC4626 vault inflation attack

## Pattern

ERC4626 vaults (and the broader family of "deposit assets, mint shares
priced as `assets * totalSupply / totalAssets`" contracts — including
Compound/Aave-style cTokens, liquid-staking vaults, and AMM-style LPs)
share a single arithmetic vulnerability: when `totalSupply` is small
and `totalAssets` can be increased without minting new shares, the
share price can be inflated to a value where subsequent deposits round
down to zero shares.

The canonical exploit is a "first-depositor donation" and runs the
same way across dozens of audited reports: the attacker (i) deposits
the smallest possible asset amount, minting a single wei of shares
that gives them 100% of `totalSupply`; (ii) directly transfers
(donates) a large quantity of the underlying asset to the vault,
inflating `totalAssets` without changing `totalSupply`; (iii)
front-runs an honest user's deposit. Because `sharesMinted =
assets * totalSupply / totalAssets` rounds down, and the victim's
deposit is now smaller than (or comparable to) the inflated
`totalAssets`, the victim receives 0 (or near-0) shares. The attacker
then redeems their 1 wei share and walks away with both the donation
and the victim's deposit. This is the exact pattern documented for
Stella, Yield Ninja, Protectorate, Steadefi, Vaultka, Narwhal,
StakePet, Persistence and many others
[solodit-trust-security-2023-05-29-stella-0-3,
solodit-pashov-audit-group-2022-11-01-yield-ninja-0-1,
solodit-pashov-audit-group-2023-06-01-protectorate-1-1,
solodit-zokyo-2024-05-15-steadefi-0-0,
solodit-zokyo-2024-03-06-vaultka-0-0,
solodit-zokyo-2023-06-09-narwhal-finance-0-0,
solodit-cyfrin-2023-09-19-cyfrin-stakepet-0-1,
solodit-hexens-2024-01-12-persistence-0-2].

The same arithmetic is exploitable in Compound v2 / Aave v2 forks the
moment a new market is listed with zero supply: an attacker mints a
tiny number of cTokens, donates a large amount of the underlying to
the cToken contract, and inflates the cToken-to-underlying exchange
rate so a 1-wei position can be used as collateral worth millions —
this is the "empty-market rounding bug" that took down Hundred
Finance, Onyx, Radiant, and (in a slightly more elaborate form)
ResupplyFi [rekt-hundred-rekt2, rekt-onyx-protocol-rekt,
rekt-radiant-capital-rekt, rekt-resupplyfi-rekt].

The defining property that makes a vault vulnerable is that
`totalAssets()` is derived from a quantity an attacker can inflate
unilaterally — usually a `balanceOf(address(this))` lookup of the
underlying token, which captures direct ERC20 transfers
[solodit-zokyo-2024-01-24-narwhal-finance-2-0,
solodit-pashov-audit-group-2023-06-01-protectorate-1-1]. If
`totalAssets()` could only ever change in lockstep with `totalSupply`,
the attack would not exist.

## Variants

### V1: Classic first-depositor donation (textbook ERC4626)

The vault has just been deployed (`totalSupply == 0`). Attacker
deposits 1 wei for 1 wei of shares, then directly transfers a large
amount of underlying to the vault. A subsequent victim deposit smaller
than the donation rounds down to 0 shares; attacker redeems and steals
the victim's deposit. Documented in essentially identical form across
Stella, Yield Ninja, Protectorate, Steadefi, Vaultka, Narwhal, Umami,
Water/Vaultka, and StakePet
[solodit-trust-security-2023-05-29-stella-0-3,
solodit-pashov-audit-group-2022-11-01-yield-ninja-0-1,
solodit-pashov-audit-group-2023-06-01-protectorate-1-1,
solodit-zokyo-2024-05-15-steadefi-0-0,
solodit-zokyo-2024-03-06-vaultka-0-0,
solodit-zokyo-2023-06-09-narwhal-finance-0-0,
solodit-zokyo-2023-04-19-umami-0-1,
solodit-zokyo-2023-08-30-vaultka-0-1,
solodit-cyfrin-2023-09-19-cyfrin-stakepet-0-1].

### V2: Empty-market exchange-rate manipulation in lending forks

Lending protocols built on Compound v2 / Aave v2 code derive
exchange-rate logic from `cash / totalSupply` of the cToken. When a
new market is listed with zero supply, an attacker takes a flash loan,
mints a small number of cTokens with the underlying, donates the rest
of the flash-loaned amount directly to the cToken contract to inflate
the exchange rate, then uses the now-overvalued cToken as collateral
to borrow the rest of the protocol's liquidity. The redeem path's
rounding error lets them recover the donation. Confirmed real-world
incidents on Hundred Finance ($7.4M), Onyx ($2.1M), Radiant ($4.5M),
and ResupplyFi ($9.8M) [rekt-hundred-rekt2, rekt-onyx-protocol-rekt,
rekt-radiant-capital-rekt, rekt-resupplyfi-rekt].

The ResupplyFi variant has an additional twist: the protocol computed
`exchangeRate = 1e36 / oracle.getPrices()`. When the donation inflated
the vault's reported price to ~2 * 10^36, floor division produced an
exchange rate of zero — and a zero exchange rate means zero
loan-to-value enforcement, allowing the attacker to borrow $10M with
1 wei of collateral [rekt-resupplyfi-rekt].

### V3: Ceiling-division dilution (no full zero-share required)

In Ubet's MarketMaker, `sharesMinted` is computed with `ceilDiv`,
which guarantees every depositor receives at least 1 share even when
the share price is inflated. An attacker deposits 1 wei to seed, then
donates a large amount, then performs many 1-wei deposits — each
minting 1 share and progressively diluting the original LP share. The
exit yields a multiple of the original deposit
[solodit-0x52-2023-12-18-ubet-0-0]. The lesson: a non-zero-shares
require is necessary but not sufficient if rounding direction favors
the attacker.

### V4: Donation as a denial-of-service / griefing primitive

When a vault relies on share-count invariants downstream of mints, an
inflation donation can break those invariants. In Strata Tranches, a
`MIN_SHARES` post-withdraw check is supposed to mitigate donation
attacks; the attacker instead deposits 1 wei, donates underlying to
the strategy, deposits 1.1e18 to mint only 1 wei of shares, and
thereafter any deposit (even 1M USDe) mints share amounts so small
they cannot stay above `MIN_SHARES` — all subsequent withdrawals
revert, trapping all deposits [solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-1-1].

### V5: Mid-life donation to manipulate fee / recovery exchange rates

The attack is not limited to fresh vaults. If the vault recomputes an
exchange rate from a balance at a critical moment (e.g. when entering
an emergency / recovery mode or when accruing fees), a donation of
underlying or wrapper shares immediately before that transition can
permanently dilute redemption value or mint excess fee shares.
Demonstrated against Lido's recovery-mode activation: a donation of
TARGET_VAULT shares between `emergencyMode` and `recoveryMode` causes
`_harvestFees` to over-mint fee shares, lowering every depositor's
redemption rate [solodit-cyfrin-2025-12-19-cyfrin-lido-earn-v2-0-0-2,
solodit-cyfrin-2025-12-19-cyfrin-lido-earn-v2-0-1-5].

### V6: Privileged operator reducing the denominator

Orbital Finance had a high-precision "denominator" intended to make
the attack uneconomic by always starting at a huge value. A malicious
operator could, however, perform an initial deposit at that high
denominator, deposit 1 wei from a second account to receive a `deltaN`
of 1, then withdraw 100% as operator — collapsing the denominator
back to 1 and resurrecting the classic donation attack against any
future depositor [solodit-trust-security-2023-05-28-orbital-finance-0-1].
The variant generalizes: defenses that rely on a "large initial
denominator" must guarantee the denominator cannot subsequently be
reduced.

### V7: Insufficient virtual-offset (defense too weak)

OpenZeppelin's `ERC4626` uses virtual shares with a `_decimalsOffset()`
hook. The default offset is 0, which (per the OZ docs) makes the
attack non-profitable but does not prevent it — value captured by the
virtual shares roughly matches the attacker's expected gains. With
`_decimalsOffset() == 6`, the attack becomes orders of magnitude more
expensive than profitable. Auditors at Zokyo flagged a vault inheriting
OZ ERC4626 with no offset override as a Low because of this gap
[solodit-zokyo-2024-10-29-liberty-finance-0-0].

### V8: First-depositor share inflation via deposit/withdraw recycling

In Beefy's concentrated-liquidity vault, the share computation
asymmetry between deposit and withdraw lets the first depositor
inflate their own share count by repeatedly depositing and withdrawing
the same tokens. Cyfrin could not find a way to steal a subsequent
depositor's tokens through this — the variant is primarily a share
accounting anomaly — but it illustrates that "first depositor" math
can produce surprising states even without theft
[solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-5].

## Defenses (and how each can fail)

Several mitigations recur across the corpus. None is unconditionally
safe; pick more than one and verify carefully.

* **Mint a chunk of shares to `address(0)` / dead address on first
  deposit** (Uniswap V2 `MINIMUM_LIQUIDITY` approach, 1000 shares). The
  most-recommended fix across reports
  [solodit-zokyo-2024-05-15-steadefi-0-0,
  solodit-zokyo-2024-03-06-vaultka-0-0,
  solodit-zokyo-2023-06-09-narwhal-finance-0-0,
  solodit-pashov-audit-group-2022-11-01-yield-ninja-0-1,
  solodit-pashov-audit-group-2023-06-01-protectorate-1-1,
  solodit-cyfrin-2023-09-19-cyfrin-stakepet-0-1]. Boundary's V2.2
  burns 1e12 shares to itself at deployment for the same reason
  [solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-1-0].

* **OpenZeppelin's virtual-shares / `_decimalsOffset` ERC4626**. Works
  when the offset is large enough; the default of 0 only neutralizes
  attacker *profit*, not the attack itself
  [solodit-zokyo-2024-10-29-liberty-finance-0-0,
  solodit-trust-security-2023-05-29-stella-0-3,
  solodit-trust-security-2023-05-28-orbital-finance-0-1].

* **Protocol-seeded first deposit** (deployer/DAO deposits a large
  amount before opening to users). Used by Umami DAO
  [solodit-zokyo-2023-04-19-umami-0-1]. Critical: deployment script
  must atomically seed before deposits are enabled, or someone will
  front-run. Recommended explicitly for Compound forks (mint
  cTokens & burn to keep `totalSupply` from ever reaching 0, in the
  same transaction that creates the market)
  [rekt-onyx-protocol-rekt, rekt-radiant-capital-rekt,
  rekt-resupplyfi-rekt].

* **Require `sharesMinted > 0`**. Necessary but insufficient — Ubet
  used `ceilDiv` to guarantee `>= 1` and was still exploitable via
  many 1-wei deposits [solodit-0x52-2023-12-18-ubet-0-0].

* **Track `totalAssets` via an internal accumulator rather than
  `token.balanceOf(this)`**. Makes donations have no effect on share
  math [solodit-zokyo-2024-01-24-narwhal-finance-2-0,
  solodit-trust-security-2023-05-28-orbital-finance-0-1 ("Tracked
  Balances" final fix)]. Watch for fee-on-transfer / rebasing tokens
  that break this invariant.

* **Per-call minimum-shares-out slippage parameter** (signed by the
  user at submit time). Defends individual users against share-rate
  manipulation between submission and execution
  [solodit-hexens-2024-01-12-persistence-0-2].

* **Enforce a minimum deposit** to make dust attacks economically
  uninteresting [solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-1-0].

## Audit checklist

* When `totalSupply == 0`, what is the formula for the first
  depositor's shares? Is `mintShares` derived from
  `assets * totalSupply / totalAssets` (or a variant), and does
  `totalAssets` include the contract's raw token balance?
* Is there any path that lets `totalSupply` return to zero or a very
  small number after the vault has been used (e.g. mass withdrawals,
  redeems, slashing)? If so, the donation attack is reachable again.
* Does the vault use OpenZeppelin's `ERC4626` with a non-default
  `_decimalsOffset()` override (≥ 6 is typical)?
  [solodit-zokyo-2024-10-29-liberty-finance-0-0]
* Does the deploy script atomically seed the vault with a
  protocol-owned deposit (or mint dead shares to `address(0)`) in the
  same transaction that enables user deposits? Or is there a window
  where the vault is live but empty? [rekt-resupplyfi-rekt,
  rekt-radiant-capital-rekt]
* For lending protocols listing a new market: does the listing
  proposal include a non-trivial initial mint-and-burn of cTokens
  with the collateral factor initially set to zero, then later
  raised? [rekt-onyx-protocol-rekt, rekt-hundred-rekt2]
* Is `totalAssets()` (or the cToken `exchangeRate` equivalent)
  computed from `IERC20.balanceOf(address(this))` — which captures
  direct donations — or from an internal accumulator that only
  changes inside `deposit`/`withdraw`?
  [solodit-zokyo-2024-01-24-narwhal-finance-2-0]
* Is the share-mint divisor's rounding direction safe? Note that
  `ceilDiv` (rounding up) is *not* a fix; it enables the variant
  where the attacker dilutes via many 1-wei deposits.
  [solodit-0x52-2023-12-18-ubet-0-0]
* Does the deposit path require `sharesMinted > 0`? Does the
  withdraw / preview path round in the protocol's favor?
* Is there a user-supplied `minSharesOut` parameter that reverts on
  manipulated rates? [solodit-hexens-2024-01-12-persistence-0-2]
* Does any downstream invariant depend on absolute share counts
  (e.g. `MIN_SHARES` post-withdraw checks)? If so, can a donation
  make legitimate deposits mint share quantities small enough to
  break the invariant and DoS withdrawals?
  [solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-1-1]
* When transitioning into a special mode (recovery, emergency,
  fee-harvest), does the contract recompute exchange rates from
  current balances? If yes, can the transition be front-run with a
  donation? [solodit-cyfrin-2025-12-19-cyfrin-lido-earn-v2-0-0-2,
  solodit-cyfrin-2025-12-19-cyfrin-lido-earn-v2-0-1-5]
* Are there privileged paths (operator / admin) that can withdraw
  100% of assets while leaving a tiny share supply behind?
  [solodit-trust-security-2023-05-28-orbital-finance-0-1]
* For oracles or LTV calculations that consume the share price: does
  any intermediate division (`1e36 / price`) floor to zero when the
  price is inflated? A zero exchange rate is interpreted as
  unconstrained borrowing in some protocols.
  [rekt-resupplyfi-rekt]

## Prior incidents

* **ResupplyFi (June 2025) — $9.8M**: classic ERC4626 donation
  against a 2-hour-old cvcrvUSD market. Attacker minted 1 wei of
  shares, donated 2,000 crvUSD, oracle reported the inflated price,
  and a `1e36 / price` calculation in the LTV path floor-divided to
  zero — letting them borrow 10M reUSD against 1 wei of collateral
  [rekt-resupplyfi-rekt].
* **Onyx Protocol (Nov 2023) — $2.1M**: empty-market attack on a
  freshly-listed PEPE cToken on a Compound v2 fork
  [rekt-onyx-protocol-rekt].
* **Radiant Capital (Jan 2024) — $4.5M**: Aave v2 fork, exploit
  contract deployed 6 seconds after activation of a new native-USDC
  market on Arbitrum. Aave itself had already patched the bug by
  always seeding new markets [rekt-radiant-capital-rekt].
* **Hundred Finance (Apr 2023) — $7.4M**: two wBTC cTokens existed;
  the unused, empty one was exploited via flash-loaned WBTC donation
  to inflate the hWBTC/WBTC exchange rate, then redeemed via a
  rounding error [rekt-hundred-rekt2].

## References

Corpus entries this synthesis derives from:

- rekt-resupplyfi-rekt
- rekt-onyx-protocol-rekt
- rekt-hundred-rekt2
- rekt-radiant-capital-rekt
- solodit-trust-security-2023-05-29-stella-0-3
- solodit-trust-security-2023-05-28-orbital-finance-0-1
- solodit-zokyo-2024-05-15-steadefi-0-0
- solodit-zokyo-2024-01-24-narwhal-finance-2-0
- solodit-zokyo-2024-03-06-vaultka-0-0
- solodit-zokyo-2023-04-19-umami-0-1
- solodit-zokyo-2023-08-30-vaultka-0-1
- solodit-zokyo-2024-10-29-liberty-finance-0-0
- solodit-zokyo-2023-06-09-narwhal-finance-0-0
- solodit-cyfrin-2023-09-19-cyfrin-stakepet-0-1
- solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-5
- solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-1-1
- solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-1-0
- solodit-cyfrin-2025-12-19-cyfrin-lido-earn-v2-0-0-2
- solodit-cyfrin-2025-12-19-cyfrin-lido-earn-v2-0-1-5
- solodit-pashov-audit-group-2023-06-01-protectorate-1-1
- solodit-pashov-audit-group-2022-11-01-yield-ninja-0-1
- solodit-0x52-2023-12-18-ubet-0-0
- solodit-hexens-2024-01-12-persistence-0-2

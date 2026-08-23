---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-12-cyfrin-paladin-valkyrie-v2-0-2-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-03-12T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-12-cyfrin-paladin-valkyrie-v2-0
title: ERC-20 tokens that do not implement `symbol()` are incompatible despite being
  accepted by Uniswap v4
vuln_class: []
---

# ERC-20 tokens that do not implement `symbol()` are incompatible despite being accepted by Uniswap v4

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-12-cyfrin-paladin-valkyrie-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-12-cyfrin-paladin-valkyrie-v2.0.md)_

---

**Description:** The protocol intends to support any ERC-20 token accepted by Uniswap v4; however, Uniswap v4 accepts tokens that do not implement the optional `symbol()` method from the ERC-20 standard.

In the following test, a Uniswap V4 pool is created with custom mocks that do not implement the `symbol()` method:
```solidity
function test_PoolCreationWithTokensWithoutSymbols() public {
    MockERC20WithoutSymbol token0WithoutSymbol = new MockERC20WithoutSymbol("TEST1", 18);
    token0WithoutSymbol.mint(address(this), 1_000_000 * 10 ** 18);
    MockERC20WithoutSymbol token1WithoutSymbol = new MockERC20WithoutSymbol("TEST2", 18);
    token1WithoutSymbol.mint(address(this), 1_000_000 * 10 ** 18);

    vm.expectRevert();
    IERC20Metadata(address(token0WithoutSymbol)).symbol();
    vm.expectRevert();
    IERC20Metadata(address(token1WithoutSymbol)).symbol();

    PoolKey memory newKey = createPoolKey(address(token0WithoutSymbol), address(token1WithoutSymbol), 3000, hookAddress);
    PoolId newId = key.toId();

    token0WithoutSymbol.approve(address(fullRange), type(uint256).max);
    token1WithoutSymbol.approve(address(fullRange), type(uint256).max);

    // address(0) is passed as the hook to prevent the revert from the actual FullRangeHook initialization
    initPool(newKey.currency0, newKey.currency1, IHooks(address(0)), 3000, SQRT_PRICE_1_1);
}
```

While Uniswap v4 supports ERC-20 tokens of this kind, neither `FullRangeHook` nor `MultiRangeHook` does as they assume the `symbol()` method can be called.

`FullRangeHook`:
```solidity
function beforeInitialize(address, PoolKey calldata key, uint160)
    external
    override
    onlyPoolManager
    returns (bytes4)
{
    ...
    // Prepare the symbol for the LP token to be deployed
    string memory symbol0 =
        key.currency0.isAddressZero() ? NATIVE_CURRENCY_SYMBOL : IERC20Metadata(Currency.unwrap(key.currency0)).symbol();
    string memory symbol1 =
        key.currency1.isAddressZero() ? NATIVE_CURRENCY_SYMBOL : IERC20Metadata(Currency.unwrap(key.currency1)).symbol();

    string memory tokenSymbol =
        string(abi.encodePacked("UniV4", "-", symbol0, "-", symbol1, "-", Strings.toString(uint256(key.fee))));
    // Deploy the LP token for the Pool
    address poolToken = address(new IncentivizedERC20(tokenSymbol, tokenSymbol, poolId));
    ...
}
```

`MultiRangeHook`:
```solidity
function createRange(PoolKey calldata key, RangeKey calldata rangeKey) external {
    ...
    // Prepare the symbol for the LP token to be deployed
    string memory symbol0 =
        key.currency0.isAddressZero() ? NATIVE_CURRENCY_SYMBOL : IERC20Metadata(Currency.unwrap(key.currency0)).symbol();
    string memory symbol1 =
        key.currency1.isAddressZero() ? NATIVE_CURRENCY_SYMBOL : IERC20Metadata(Currency.unwrap(key.currency1)).symbol();

    string memory tokenSymbol =
        string(abi.encodePacked("UniV4", "-", symbol0, "-", symbol1, "-", Strings.toString(uint256(key.fee))));
    // Deploy the LP token for the Pool
    address lpToken = address(new IncentivizedERC20(tokenSymbol, tokenSymbol, poolId));
    ...
}
```

**Impact:** The severity of this issue is high because these tokens can not be used even though Uniswap supports them; however, the likelihood is low since it is relatively uncommon for the `symbol()` method to not be implemented, so the overall impact is medium.

**Proof of Concept:** The following test, modified from above to now use the `FullRangeHook` which reverts upon initialization, should be added to `FullRangeHook.t.sol`:
```solidity
function test_PoolCreationWithTokensWithoutSymbols() public {
    MockERC20WithoutSymbol token0WithoutSymbol = new MockERC20WithoutSymbol("TEST1", 18);
    token0WithoutSymbol.mint(address(this), 1_000_000 * 10 ** 18);
    MockERC20WithoutSymbol token1WithoutSymbol = new MockERC20WithoutSymbol("TEST2", 18);
    token1WithoutSymbol.mint(address(this), 1_000_000 * 10 ** 18);

    vm.expectRevert();
    IERC20Metadata(address(token0WithoutSymbol)).symbol();
    vm.expectRevert();
    IERC20Metadata(address(token1WithoutSymbol)).symbol();

    PoolKey memory newKey = createPoolKey(address(token0WithoutSymbol), address(token1WithoutSymbol), 3000, hookAddress);
    PoolId newId = key.toId();

    token0WithoutSymbol.approve(address(fullRange), type(uint256).max);
    token1WithoutSymbol.approve(address(fullRange), type(uint256).max);

    vm.expectRevert();
    initPool(newKey.currency0, newKey.currency1, IHooks(address(fullRange)), 3000, SQRT_PRICE_1_1);
}
```
The `MockERC20WithoutSymbol` is required for the test to run and trivial to reproduce.

**Recommended Mitigation:** It is recommended to implement a `try/catch` structure to verify whether the given token implements the `symbol()` method. If it is not supported, a default symbol could be used instead.

**Paladin:** Acknowledged, but as said in the issue, it is relatively uncommon to encounter an ERC20 that does not implement the `symbol()` function, so we accept not to support those tokens with our Hooks, as Pools for those rare tokens could be connected to Valkyrie via the Subscriber, or another Hook that will handle this edge case => No changes done here.

**Cyfrin:** Acknowledged.

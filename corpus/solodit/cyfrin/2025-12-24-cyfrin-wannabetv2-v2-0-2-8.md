---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-wannabetv2-v2-0-2-8
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-wannabetv2-v2-0
title: '`BetFactory::setPool` should validate input pool is legitimate AaveV3 pool
  and supports input token'
vuln_class: []
---

# `BetFactory::setPool` should validate input pool is legitimate AaveV3 pool and supports input token

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-wannabetv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md)_

---

**Description:** `BetFactory::setPool` should validate input pool is legitimate AaveV3 pool and supports input token. This can be done by:

1) `BetFactory::constructor` should take as input the address of AaveV3 deployed `PoolAddressesProvider` contract and store it into an immutable variable `AAVE_ADDRESSES_PROVIDER`; on Base mainnet this is `0xe20fCBdBfFC4Dd138cE8b2E6FBb6CB49777ad64D`

2) `BetFactory::setPool` should verify that input `_pool` matches `PoolAddressesProvider::getPool`

3) `BetFactory::setPool` should verify that input `_token` is an associated underlying token of the pool by calling `Pool::getReserveAToken` and ensuring the return value is not `address(0)`

4) optionally also verify via `IAToken::UNDERLYING_ASSET_ADDRESS`

**Recommended Mitigation:** A potential solution which appears to work with the existing test suite, and also resolves finding M-3:

1) first add these additional includes to `BetFactory.sol`:
```solidity
import {IPool} from "@aave-dao/aave-v3-origin/src/contracts/interfaces/IPool.sol";
import {IAToken} from "@aave-dao/aave-v3-origin/src/contracts/interfaces/IAToken.sol";
import {IPoolAddressesProvider} from "@aave-dao/aave-v3-origin/src/contracts/interfaces/IPoolAddressesProvider.sol";
```

2) Inside `BetFactory`, define this constant and three new errors:
```solidity
contract BetFactory is Ownable {
    // Base mainnet Aave V3 PoolAddressesProvider
    IPoolAddressesProvider public constant AAVE_ADDRESSES_PROVIDER =
        IPoolAddressesProvider(0xe20fCBdBfFC4Dd138cE8b2E6FBb6CB49777ad64D);

    error InvalidPool();
    error TokenNotSupported();
    error ATokenMismatch();
```

3) Use this new version for `BetFactory::setPool`:
```solidity
    function setPool(address _token, address _pool) external onlyOwner {
        // Allow setting to zero (disable Aave for this token)
        if (_pool == address(0)) {
            tokenToPool[_token] = address(0);
            emit PoolConfigured(_token, address(0));
            return;
        }

        // Validate against canonical registry
        if (_pool != AAVE_ADDRESSES_PROVIDER.getPool()) {
            revert InvalidPool();
        }

        // Verify token is listed
        address aToken = IPool(_pool).getReserveAToken(_token);
        if (aToken == address(0)) {
            revert TokenNotSupported();
        }

        // Verify bidirectional relationship
        if (IAToken(aToken).UNDERLYING_ASSET_ADDRESS() != _token) {
            revert ATokenMismatch();
        }

        tokenToPool[_token] = _pool;
        emit PoolConfigured(_token, _pool);
    }
```

**WannaBet:** Fixed in commit [70e1565](https://github.com/gskril/wannabet-v2/commit/70e1565b391992b7ea8b11f2cc59195478a69212).

**Cyfrin:** Verified.

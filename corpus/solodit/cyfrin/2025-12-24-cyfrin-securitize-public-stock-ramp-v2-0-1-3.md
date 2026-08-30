---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-1-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: Signatures used in `PublicStockOnRamp` and `PublicStockOffRamp` lack investor-specified
  deadline and nonce parameters so can be used multiple times by operators
vuln_class: []
---

# Signatures used in `PublicStockOnRamp` and `PublicStockOffRamp` lack investor-specified deadline and nonce parameters so can be used multiple times by operators

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** Both `PublicStockOnRamp` and `PublicStockOffRamp` contracts use EIP-712 signatures to authorize investor transactions. However, these signatures do not include a deadline/expiration parameter in their signed data structure, making them valid indefinitely until executed.
In  `PublicStockOnRamp`, the signature only includes the liquidity amount and minimum output amount:

```solidity
bytes32 private constant TXTYPE_HASH = keccak256("Swap(uint256 liquidityAmount,uint256 minOutAmount)");

  function hashTx(uint256 _liquidityAmount, uint256 _minOutAmount) private view returns (bytes32) {
        bytes32 structHash = keccak256(
            abi.encode(TXTYPE_HASH, _liquidityAmount, _minOutAmount)
        );

        return _hashTypedDataV4(structHash);
    }
```

Similarly in `PublicStockOffRamp`:

```solidity
bytes32 private constant TXTYPE_HASH = keccak256("Redeem(uint256 assetAmount,uint256 minOutputAmount)");

function hashTx(uint256 _assetAmount, uint256 _minOutputAmount) private view returns (bytes32) {
        bytes32 structHash = keccak256(
            abi.encode(TXTYPE_HASH, _assetAmount, _minOutputAmount)
        );

        return _hashTypedDataV4(structHash);
    }
```

While both contracts have `_anchorPriceExpiresAt` as a function parameter to ensure the price feed isn't stale, this expiration is not part of the signed message. An investor's signature remains valid indefinitely and can be executed at any future time by an operator, as long as they provide a valid (non-expired) anchor price.
Additionally, there is no nonce mechanism in either contract to allow investors to invalidate/cancel previously signed transactions.

**Impact:** Once an investor signs a transaction, they cannot invalidate it even if market conditions change significantly, An operator could hold onto a signature for days/weeks/months and execute it at an inopportune time for the investor. Because there is no nonce used the operator could use the investor's signature to execute multiple transactions.

**Recommended Mitigation:** Include a deadline parameter in the signed message structure and implement a nonce perhaps using [NoncesUpgradeable](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/master/contracts/utils/NoncesUpgradeable.sol) or similar to how `SecuritizeOnRamp` does it via the mapping `noncePerInvestor`. Since `PublicStockOnRamp` and `SecuritizeOnRamp` both inherit from `BaseOnRamp`, it may be ideal to move the common functionality into there.

**Securitize:** Fixed in commit [85142ed](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/85142edf57f24a4af30f2e46382188adac60fbc2).

**Cyfrin:** Verified.

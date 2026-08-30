---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-4-11
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-09-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-01-cyfrin-licredity-v2-0
title: Dirty bits in `NonFungible` mid-field can break comparisons
vuln_class: []
---

# Dirty bits in `NonFungible` mid-field can break comparisons

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-01-cyfrin-licredity-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md)_

---

**Description:** [`NonFungible`](https://github.com/Licredity/licredity-v1-core/blob/e8ae10a7d9f27529e39ca277bf56cef01a807817/src/types/NonFungible.sol#L8-L16) is packed as `bytes32` with the layout `160 bits address | 32 bits empty | 64 bits tokenId`. Equality is implemented as a raw `bytes32` comparison:
```solidity
/// @dev 160 bits token address | 32 bits empty | 64 bits token ID
type NonFungible is bytes32;

...

function equals(NonFungible self, NonFungible other) pure returns (bool) {
    return NonFungible.unwrap(self) == NonFungible.unwrap(other);
}
```
Because the 32-bit middle segment is unused, any non-zero “dirty bits” left there will cause otherwise identical `(address, tokenId)` pairs to compare unequal. This can break lookups and equality checks across modules that don’t canonicalize the encoding. This can lead to hard-to-diagnose issues like unsuccessful removals from arrays/sets. We did not find a direct exploit path, but it’s a footgun that can surface as integration bugs.

Consider adopting a canonical encoding and/or canonical equality:

* Easiest: consume the gap by widening `tokenId` to 96 bits so the entire word is meaningful.

  ```solidity
  // 160 bits addr | 96 bits id
  function pack(address token, uint256 id) pure returns (NonFungible nf) {
      uint256 w = (uint256(uint160(token)) << 96) | (id & ((1 << 96) - 1));
      return NonFungible.wrap(bytes32(w));
  }
  ```
* Or keep the 64-bit id, but zero the gap on pack and mask on equals:

  ```solidity
  uint256 constant MASK_ADDR  = uint256(type(uint160).max) << 96;
  uint256 constant MASK_ID64  = uint256(type(uint64).max);
  uint256 constant MASK_CANON = MASK_ADDR | MASK_ID64;

  function pack(address token, uint256 id) pure returns (NonFungible nf) {
      uint256 w = (uint256(uint160(token)) << 96) | (id & MASK_ID64); // gap zeroed
      return NonFungible.wrap(bytes32(w));
  }

  function equals(NonFungible a, NonFungible b) pure returns (bool) {
      return (uint256(NonFungible.unwrap(a)) & MASK_CANON)
           == (uint256(NonFungible.unwrap(b)) & MASK_CANON);
  }
  ```

Either approach ensures different encoders produce the same canonical value and equality is robust.

**Licredity:** Fixed in [PR#66](https://github.com/Licredity/licredity-v1-core/pull/66/files) and [PR#77](https://github.com/Licredity/licredity-v1-core/pull/77/files) commits [`7498ea0`](https://github.com/Licredity/licredity-v1-core/commit/7498ea007b4ad6975653bea08e27c2899f6bc413) and [`9be45ef`](https://github.com/Licredity/licredity-v1-core/commit/9be45efe7986e34bd184de151fa2d5dd3f81e9db)

**Cyfrin:** Verified. Middle 32 bits are now ignored when comparing.

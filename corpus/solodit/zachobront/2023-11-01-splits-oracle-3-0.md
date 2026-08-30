---
affected_contracts: []
derives_from: []
id: solodit-zachobront-2023-11-01-splits-oracle-3-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-11-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-splits-oracle.md
tags:
- firm:zachobront
- report:2023-11-01-splits-oracle
title: '[I-01] Extra bytes can be included in pairDetails'
vuln_class: []
---

# [I-01] Extra bytes can be included in pairDetails

_Section severity (from Solodit section header): Informational_  
_Audit firm: ZachObront_  
_Source report: [2023-11-01-splits-oracle.md](https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-splits-oracle.md)_

---

When `$_pairDetails` are set, we store a bytestring (which represents a packed version of an array of Feeds) and an `inverted` boolean flag.

Before storing these values, we use `path.getFeeds()` to decode the bytestring into an array of Feeds and validate that the parameters passed are valid (ie that decimals equals the decimals on the feed and that `staleAfter` > 1 hour).

When these values are accessed, we also use the `path.getFeeds()` function to retrieve the feeds for oracle price calculations.

If we look at the implementation of `getFeeds()`, we can see that it first gets the number of feeds in the path, and then iterates over each of these feeds, calling `getFeed()` to decode and return it:
```solidity
/// @notice get feeds from a path (packed encoded bytes)
function getFeeds(bytes memory path) internal pure returns (ChainlinkOracleImpl.Feed[] memory feeds) {
    uint256 length = len(path);
    feeds = new ChainlinkOracleImpl.Feed[](length);
    for (uint256 i; i < length;) {
        feeds[i] = getFeed(path, i);
        unchecked {
            ++i;
        }
    }
}
```
```solidity
/// @notice get the number of feeds in the path
function len(bytes memory path) internal pure returns (uint256) {
    return path.len(PATH_UNIT_SIZE);
}
```
```solidity
function len(bytes memory _bytes, uint256 _size) internal pure returns (uint256) {
    return _bytes.length / _size;
}
```
If the length of the bytearray passed is not evenly divisible by 25, the extra bytes will be ignored by `getFeeds()`. This will skip validation, store the bytes in storage, and also skip returning them to be used when the oracle is called.

I do not see any harm in these extra bytes existing, but in the event that extra interactions are implemented at a later date or there is a risk I'm not seeing, it would be more precise and safer to require that bytestrings passed do not contain extra bytes.

**Recommendation**

```diff
/// @notice get the number of feeds in the path
function len(bytes memory path) internal pure returns (uint256) {
+   if (path.length % 25 != 0) revert ExtraBytesInPath();
    return path.len(PATH_UNIT_SIZE);
}
```

**Review**

[Fixed by performing recommended check directly in BytesLib.](https://github.com/0xSplits/splits-oracle/commit/aaff90ef0727918ba3e26069ba84ad88d85a8fec)

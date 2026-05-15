---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-1-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: '`LibTokenPermit` logic is susceptible to signature replay attacks in the case
  of a hard fork'
vuln_class: []
---

# `LibTokenPermit` logic is susceptible to signature replay attacks in the case of a hard fork

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

**Description:** Due to the implementation of [`LibTokenPermit::_buildDomainSeparator`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Token/LibTokenPermit.sol#L59-L69) using the static `CHAIN_ID` [constant](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Token/LibTokenPermit.sol#L65) specified in [`C.sol`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/C.sol#L92-L94), in the case of a hard fork, all signed permits from Ethereum mainnet can be replayed on the forked chain.

**Impact:** A signature replay attack on the forked chain means that any signed permit given to an address on one of the chains can be re-used on the other as long as the account nonce is respected. Given that BEAN has a portion of its liquidity in WETH, it could be susceptible to some parallelism with the [Omni Bridge calldata replay exploit](https://medium.com/neptune-mutual/decoding-omni-bridges-call-data-replay-exploit-f1c7e339a7e8) on ETHPoW.

**Recommended Mitigation:** Modify the `_buildDomainSeparator` implementation to read the current `block.chainid` global context variable directly. If gas efficiency is desired, it is recommended to cache the current chain id on contract creation and only recompute the domain separator if a change of chain id is detected (i.e. `block.chainid` != cached chain id).

```diff
    function _buildDomainSeparator(bytes32 typeHash, bytes32 name, bytes32 version) internal view returns (bytes32) {
        return keccak256(
            abi.encode(
                typeHash,
                name,
                version,
-               C.getChainId(),
+               block.chainid,
                address(this)
            )
        );
    }
```

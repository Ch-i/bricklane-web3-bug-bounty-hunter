---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-2-8
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Unchecked decrement results in integer underflow in `LibStrings::toString`
vuln_class: []
---

# Unchecked decrement results in integer underflow in `LibStrings::toString`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

**Description:** The implementation of [`LibStrings::toString`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/LibStrings.sol#L16-L37) is intended to convert an unsigned integer to its string representation. If the value provided is non-zero, the function determines the number of digits in the number, creates a byte buffer of the appropriate size, and then populates that buffer with the ASCII representation of each digit. However, given Beanstalk uses a Solidity compiler version lower than `0.8.0` in which safe, checked math was introduced as default, this library is susceptible to over/underflow of unchecked math operations. One such issue arises when [post-decrementing the `index`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/LibStrings.sol#L33), initialized as [`digits - 1`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/LibStrings.sol#L30), which underflows on the final loop iteration.


**Impact:** Evidence of underflow is visible in the use of this function on-chain in both `MetadataFacet::uri`:

![URI](img/uri.png)

and `MetadataImage::imageURI`:

![Image](img/overlap.png)

The "Deposit stem" [attribute](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/metadata/MetadataFacet.sol#L37) is incredibly large due to wrap-around of the maximum `uint256` value, and the same issue applies to [`MetadataImage::blackBars`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/metadata/MetadataImage.sol#L528) called within [`MetadataImage::generateImage](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/metadata/MetadataImage.sol#L35-L49) which causes the stem string representation to overlap with the ["Bean Deposit" text](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/metadata/MetadataImage.sol#L538-L539).

This issue should be resolved to display accurate metadata, given the following disclaimer in `MetadataFacet::uri`:
> DISCLAIMER: Due diligence is imperative when assessing this NFT. Opensea and other NFT marketplaces cache the svg output and thus, may require the user to refresh the metadata to properly show the correct values."

**Recommended Mitigation:** Initialize `index` to `digits` and pre-decrement instead to avoid underflow on the final loop iteration.

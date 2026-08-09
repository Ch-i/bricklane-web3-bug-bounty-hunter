---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-cryptoart-v2-0-1-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-cryptoart-v2-0
title: Prevent code-injection inside `string` fields when emitting `IStory` events
  or setting `tokenURI` fields
vuln_class: []
---

# Prevent code-injection inside `string` fields when emitting `IStory` events or setting `tokenURI` fields

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-cryptoart-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-cryptoart-v2.0.md)_

---

**Description:** An attack vector which spans the intersection between web3 and web2 is when users can [associate arbitrary metadata strings with NFTs](https://medium.com/zokyo-io/under-the-hackers-hood-json-injection-in-nft-metadata-3be78d0f93a7) and those strings are later processed or displayed on a website.

In particular the `IStory::Story` event:
* is emitted by a non-trusted entity, the current holder of the artwork
* emits two arbitrary string parameters, `collectorName` and `story`
* these string parameters are designed to be displayed to users and may be processed by web2 apps

**Recommended Mitigation:** The most important validation is for non-trusted user-initiated functions, eg:
* When a Creator emits `CreatorStory` or a Collector emits `Story`, revert if the `name` and `story` strings contain any unexpected special characters
* When minting tokens revert if `TokenURISet::uriWhenRedeemable` and `uriWhenNotRedeemable` contain any unexpected special characters - though this must be done using off-chain components controlled by the protocol so risk here is minimal
* In off-chain code don't trust any user-supplied strings but sanitize them or check them for unexpected special characters

**CryptoArt:**
Acknowledged; mitigation handled off-chain via URI validation pre-signing, Story string sanitization/encoding post-event.

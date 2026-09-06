---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-24-cyfrin-linea-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-05-24T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md
tags:
- firm:cyfrin
- report:2024-05-24-cyfrin-linea
title: Deprecated variable `L1MessageServiceV1::__messageSender` is still used making
  `TokenBridge::completeBridging` revert for older messages preventing users from
  receiving bridged tokens
vuln_class: []
---

# Deprecated variable `L1MessageServiceV1::__messageSender` is still used making `TokenBridge::completeBridging` revert for older messages preventing users from receiving bridged tokens

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-24-cyfrin-linea.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md)_

---

**Description:** In `L1MessageServiceV1`, this [comment](https://github.com/Consensys/zkevm-monorepo/blob/364b64d2a2704567adac00e3fa428a1901717666/contracts/contracts/messageService/l1/v1/L1MessageServiceV1.sol#L27) indicates that `_messageSender` storage variable is deprecated in favor of transient storage.

However the deprecated `_messageSender` is [updated](https://github.com/Consensys/zkevm-monorepo/blob/364b64d2a2704567adac00e3fa428a1901717666/contracts/contracts/messageService/l1/v1/L1MessageServiceV1.sol#L122) in `L1MessageServiceV1::claimMessage` and also [set](https://github.com/Consensys/zkevm-monorepo/blob/364b64d2a2704567adac00e3fa428a1901717666/contracts/contracts/messageService/l1/L1MessageService.sol#L68) in `L1MessageService::__MessageService_init`. But `L1MessageService::claimMessageWithProof` does [use](https://github.com/Consensys/zkevm-monorepo/blob/364b64d2a2704567adac00e3fa428a1901717666/contracts/contracts/messageService/l1/L1MessageService.sol#L142) the transient storage method.

`MessageServiceBase::onlyAuthorizedRemoteSender` [calls](https://github.com/Consensys/zkevm-monorepo/blob/364b64d2a2704567adac00e3fa428a1901717666/contracts/contracts/messageService/MessageServiceBase.sol#L52-L57) `L1MessagingService::sender` to retrieve the message sender and this function always [fetches](https://github.com/Consensys/zkevm-monorepo/blob/364b64d2a2704567adac00e3fa428a1901717666/contracts/contracts/messageService/l1/L1MessageService.sol#L166-L168) it from transient storage and not from the deprecated `_messageSender`.

`MessageServiceBase::onlyAuthorizedRemoteSender` in turn is used by `TokenBridge`::[setDeployed](https://github.com/Consensys/zkevm-monorepo/blob/364b64d2a2704567adac00e3fa428a1901717666/contracts/contracts/tokenBridge/TokenBridge.sol#L302) and [`completeBridging`](https://github.com/Consensys/zkevm-monorepo/blob/364b64d2a2704567adac00e3fa428a1901717666/contracts/contracts/tokenBridge/TokenBridge.sol#L241).

**Impact:** Older L2->L1 messages using `claimMessage` to call `TokenBridge::setDeployed` and `completeBridging` will always revert since:
* the message sender will be fetched from transient storage
* `claimMessage` never sets message sender in transient storage as it still updates the deprecated `_messageSender` storage variable

As `completeBridging` will always revert for these transactions, users will never receive their bridged tokens.

**Recommended Mitigation:** Change `L1MessageServiceV1::claimMessage` to store message sender in transient storage and remove all uses of deprecated `_messageSender`.

**Linea:**
Fixed in commit [55d936a](https://github.com/Consensys/zkevm-monorepo/pull/3191/commits/55d936a47ca31952cc65cc9ee1c7629b919c6aa2#diff-e9f6a0c3577321e5aa88a9d7e12499c2c4819146062e33a99576971682396bb5R122-R144) merged in [PR3191](https://github.com/Consensys/zkevm-monorepo/pull/3191/files#diff-e9f6a0c3577321e5aa88a9d7e12499c2c4819146062e33a99576971682396bb5R119-R141).

**Cyfrin:** Verified.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-0-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-10-07T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0
title: Hard-coding 0 max fee with fast finality is incompatible as this combination
  commonly has minimum fees of 1
vuln_class: []
---

# Hard-coding 0 max fee with fast finality is incompatible as this combination commonly has minimum fees of 1

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** Circle's [CCTPv2 Technical Guide](https://developers.circle.com/cctp/technical-guide) provides the following relevant information:
* Messages with `minFinalityThreshold` of 1000 or lower are considered Fast messages
* Messages with `minFinalityThreshold` of 2000 are considered Standard messages (in practice everything > 1000 is considered Standard)
* The applicable fee should be retrieved every time before executing a transaction using this [API](https://developers.circle.com/api-reference/cctp/all/get-burn-usdc-fees)

The provided API requires specifying the CCTP input and output [domains](https://developers.circle.com/cctp/cctp-supported-blockchains#cctp-v2-supported-domains). Using the `wget` form of the API, the minimum fees for fast finality (1000) are typically 1:

* Ethereum -> Avalanche
```console
$ wget --quiet \
  --method GET \
  --header 'Content-Type: application/json' \
  --output-document \
  - https://iris-api-sandbox.circle.com/v2/burn/USDC/fees/0/1
[{"finalityThreshold":1000,"minimumFee":1},{"finalityThreshold":2000,"minimumFee":0}]%
```

* Ethereum -> Solana
```console
$ wget --quiet \
  --method GET \
  --header 'Content-Type: application/json' \
  --output-document \
  - https://iris-api-sandbox.circle.com/v2/burn/USDC/fees/0/5
[{"finalityThreshold":1000,"minimumFee":1},{"finalityThreshold":2000,"minimumFee":0}]%
```

**Impact:** Many CCTP cross-domain transfers have a minimum fee of 1 for fast finality, but `USDCBridgeV2::_transferUSDC` hard-codes a maximum fee of 0 with fast finality 1000:
```solidity
circleTokenMessenger.depositForBurn(
    _amount,
    getCCTPDomain(_targetChain),
    targetAddressBytes32,        // mintRecipient on destination
    USDC,          // burnToken
    destinationCallerBytes32,        // destinationCaller (restrict who can mint)
    0,   // @audit maximum fee
    1000 // @audit fast finality
);
```

This combination is incompatible and will result in many cross-domain transfers unable to use fast finality, reverting to standard finality. If the minimum fee for standard finality ever becomes > 0, this would cause all attempted cross-domain transfers to revert since the automatic downgrade to standard finality would no longer be possible.

**Recommended Mitigation:** Ideally the maximum fee and finality should be provided as inputs:
* current fee bps should be retrieved off-chain using the provided API for the desired domain combination
* multiply fee bps by the amount to be transferred to calculate the maximum fee
* pass maximum fee and desired finality as inputs when calling `circleTokenMessenger.depositForBurn`

At least there should be a way to change the maximum fee, it shouldn't be hard-coded to zero as this causes the protocol to become unusable if standard finality fees become non-zero.

**Securitize:** Fixed in commit [0d3e50d](https://github.com/securitize-io/bc-securitize-bridge-sc/commit/0d3e50daadb37b29266a86d76a9c060eeed5805d) by:
* always using standard finality
* max fee is now a variable so we can change it if Circle increases standard finality fees in the future

**Cyfrin:** Verified.

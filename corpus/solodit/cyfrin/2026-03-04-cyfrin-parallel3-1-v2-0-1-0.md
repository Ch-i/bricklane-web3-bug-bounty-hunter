---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-parallel3-1-v2-0-1-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-parallel3-1-v2-0
title: User can bypass fee and spend limits in `BridgeableTokenP`
vuln_class: []
---

# User can bypass fee and spend limits in `BridgeableTokenP`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-parallel3.1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md)_

---

**Description:** When OFT receives message, it spends credit limit and mints Principal. Interesting that it mints OFT if limits don't allow to mint Principal, moreover it applies fee only on Principal amount:
```solidity
    function _credit(
        address _to,
        uint256 _amountLD,
        uint32, //_srcEid,
        bool _isFeeApplicable
    ) private returns (uint256 amountReceived, uint256 oftReceived, uint256 feeAmount) {
        (amountReceived, feeAmount) = _handleCreditPrincipalToken(_to, _amountLD, _isFeeApplicable);

@>      oftReceived = _amountLD - amountReceived - feeAmount;
        /// If OftReceived > 0 we must be credit to the user OFT tokens to match the total amount he must be credited.
        if (oftReceived > 0) {
            _mint(_to, oftReceived);
        }
    }

    function _handleCreditPrincipalToken(
        address _to,
        uint256 _amountLD,
        bool _isFeeApplicable
    ) private returns (uint256 amountReceived, uint256 feeAmount) {
        amountReceived = _calculatePrincipalTokenAmountToCredit(_amountLD);

        if (amountReceived > 0) {
            dailyCreditAmount[_getCurrentDay()] += amountReceived;
            creditDebitBalance += int256(amountReceived);
@>          if (_isFeeApplicable) {
                if (feesRate > 0) {
                    feeAmount = amountReceived.percentMul(feesRate);
                    amountReceived -= feeAmount;
                    _creditPrincipalToken(feesRecipient, feeAmount);
                }
            }
            _creditPrincipalToken(_to, amountReceived);
        }
    }
```
And, by design, fee is not applied if origin token is OFT.

Such design introduces certain attack vectors if credit limit is hit on destination chain:
1) I have OFT on chain1, swap to Principal costs fee. I can bridge to chain2 and receive OFT, then bridge OFT from chain2 to chain1. That's how I swapped avoiding fee, moreover credit limit on chain1 can be spent to max.
2) I have Principal on chain1 and want to receive Principal on chain2. In usual scenario I will: a) bridge and receive OFT, wait next day (to refresh limit) and swap to Principal; b) wait next day and bridge directly to Principal, again pay fee. However I can do following: bridge to chain2 and receive OFT, bridge back and receive Principal - repeat until credit limit is hit, so in the end I receive OFT on chain1, wait next day and bridge OFT to Principal without fee. This way it spends both debit and credit limit on chain1.

**Impact:** User can avoid fee and spend limits if credit limit on destination chain is hit.

**Recommended Mitigation:** Maybe it should mint OFT on destination chain if origin token is OFT.

**Parallel:** We decided to acknowledge it because we expect the limits to never be reached, and at the same time, we prefer to skip some fees rather than charge users who get front-run.

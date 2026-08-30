---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-10-cyfrin-thermae-4-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-01-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-10-cyfrin-thermae.md
tags:
- firm:cyfrin
- report:2024-01-10-cyfrin-thermae
title: Use custom errors instead of revert error strings
vuln_class: []
---

# Use custom errors instead of revert error strings

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-10-cyfrin-thermae.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-10-cyfrin-thermae.md)_

---

**Description:** Using custom errors instead of revert error strings to reduce deployment and runtime cost:

```solidity
File: Portico.sol

64:         require(token.approve(spender, 0), "approval reset failed");

67:       require(token.approve(spender, 2 ** 256 - 1), "infinite approval failed");

185:     require(poolExists, "Pool does not exist");

215:       require(value == params.amountSpecified + whMessageFee, "msg.value incorrect");

225:       require(value == whMessageFee, "msg.value incorrect");

232:       require(params.startTokenAddress.transferFrom(_msgSender(), address(this), params.amountSpecified), "transfer fail");

240:       require(amount >= params.amountSpecified, "transfer insufficient");

333:     require(unpadAddress(transfer.to) == address(this) && transfer.toChain == wormholeChainId, "Token was not sent to this address");

420:         require(sentToUser, "Failed to send Ether");

425:         require(sentToRelayer, "Failed to send Ether");

432:         require(finalToken.transfer(recipient, finalUserAmount), "STF");

436:         require(finalToken.transfer(feeRecipient, relayerFeeAmount), "STF");
```

**Wormhole:**
Error strings have all been confirmed to be length < 32, this is sufficient for the purposes of this contract.

\clearpage

---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-06-01-protectorate-3-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-06-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-06-01-Protectorate.md
tags:
- firm:pashov-audit-group
- report:2023-06-01-protectorate
title: '[L-03] Trust assumption in `DutchAuction`'
vuln_class: []
---

# [L-03] Trust assumption in `DutchAuction`

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-06-01-Protectorate.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-06-01-Protectorate.md)_

---

The `DutchAuction` contract expects to be holding `auctionDetails.totalTokens` balance of `PRTC` to work correctly, but this is not validated in any way. Also, on failed auction, `auctionDetails.totalTokens` is the amount of `PRTC` sent to the beneficiary, and if the amount is even 1 wei less it would revert. I suggest using `prtc.balanceOf(address(this))` instead and also you can consider transferring the `PRTC` tokens into the contract in its constructor so it is trustless.

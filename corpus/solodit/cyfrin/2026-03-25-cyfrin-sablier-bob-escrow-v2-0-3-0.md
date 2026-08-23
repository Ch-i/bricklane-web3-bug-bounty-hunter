---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-3-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: '`SablierEscrow` buyers and sellers can''t set max fee slippage'
vuln_class: []
---

# `SablierEscrow` buyers and sellers can't set max fee slippage

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** The comptroller can change trade fees via `SablierEscrow::setTradeFee` however buyers and sellers can't set their preferred max fee slippage.

Hence the comptroller could front-run a call to `SablierEscrow::fillOrder` by increasing the fee such that the buyer and seller receive less tokens than expected, or the fee could be changed organically after the order was created but before it was filled.

That said there is a hardcoded `MAX_TRADE_FEE` which does offer some protection.

**Recommended Mitigation:** Consider allowing the buyers and sellers to set a `maxTradeFee` parameter which prevents the order from being filled if the current trade fee is greater. Alternatively consider snapshotting the current fee at creation time similar to `SablierLidoAdapter::registerVault`.

**Sablier:** Acknowledged; not allowing traders to set max trade slippage is a business decision. Since the fee cannot exceed `MAX_TRADE_FEE`, if we set it to 2% (thats what we will do it in practice), it should mitigate the issue of charging high fees.

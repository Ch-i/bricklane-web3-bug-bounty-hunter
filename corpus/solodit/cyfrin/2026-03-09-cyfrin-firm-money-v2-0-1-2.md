---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-09-cyfrin-firm-money-v2-0-1-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-09-cyfrin-firm-money-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-09-cyfrin-firm-money-v2-0
title: '`MetadataNFT` reuses wrong protocol branding'
vuln_class: []
---

# `MetadataNFT` reuses wrong protocol branding

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-09-cyfrin-firm-money-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-09-cyfrin-firm-money-v2.0.md)_

---

**Description:** The `MetadataNFT::uri` function contains hardcoded Liquity V2 branding in the NFT metadata. The title reads "Liquity V2 - " and the description references "Liquity V2 is a collateralized debt platform" and "to their own Ethereum address". This branding is inaccurate for the Firm Money deployment on Status Network L2.

https://github.com/firm-money/firm/blob/main/contracts/src/NFTMetadata/MetadataNFT.sol#L36-L49

```solidity
return json.formattedMetadata(
    string.concat("Liquity V2 - ", IERC20Metadata(_troveData._collToken).name()),
    string.concat(
        "Liquity V2 is a collateralized debt platform. Users can lock up ",
        IERC20Metadata(_troveData._collToken).symbol(),
        " to issue stablecoin tokens (BOLD) to their own Ethereum address. ..."
    ),
    renderSVGImage(_troveData),
    attr
);
```

**Impact:** Trove NFTs will display incorrect protocol branding and network references. This affects user-facing metadata on NFT marketplaces and wallets.

**Recommended Mitigation:** Update the branding to reflect the Firm Money protocol and Status Network.

**Firm Money:**
Fixed in commit [a04706b](https://github.com/firm-money/firm/pull/15/changes/a04706b5128046785e5df37a9266ccd69367e9f0).

**Cyfrin:** Verified.

\clearpage

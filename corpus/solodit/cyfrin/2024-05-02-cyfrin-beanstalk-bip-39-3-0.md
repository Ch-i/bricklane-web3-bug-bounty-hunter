---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-02-cyfrin-beanstalk-bip-39-3-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-05-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md
tags:
- firm:cyfrin
- report:2024-05-02-cyfrin-beanstalk-bip-39
title: Incorrect storage slot annotation in `Storage::SiloSettings`
vuln_class: []
---

# Incorrect storage slot annotation in `Storage::SiloSettings`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-02-cyfrin-beanstalk-bip-39.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md)_

---

While it appears that the order struct members in storage have not changed, the storage slot annotation of [`Storage::SiloSettings`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/beanstalk/AppStorage.sol#L393-L404) in `AppStorage.sol` is incorrect and should be updated as follows:

```diff
struct SiloSettings {
    bytes4 selector; // ─────────────┐ 4
-   uint32 stalkEarnedPerSeason; //  │ 4  (16)
+   uint32 stalkEarnedPerSeason; //  │ 4  (8)
-   uint32 stalkIssuedPerBdv; //     │ 4  (8)
+   uint32 stalkIssuedPerBdv; //     │ 4  (12)
-   uint32 milestoneSeason; //       │ 4  (12)
+   uint32 milestoneSeason; //       │ 4  (16)
    int96 milestoneStem; //          │ 12 (28)
    bytes1 encodeType; // ───────────┘ 1  (29)
    // 3 bytes are left here.
    uint128 gaugePoints; //   ────--------───┐ 16
    bytes4 gpSelector; //                    │ 4   (20)
    uint96 optimalPercentDepositedBdv; // ───┘ 12  (32)
}
```

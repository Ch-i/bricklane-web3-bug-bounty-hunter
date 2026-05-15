---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: The names of numerous state variables should be changed to more verbose alternatives
vuln_class: []
---

# The names of numerous state variables should be changed to more verbose alternatives

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

Currently, it can be confusing when referencing values in storage as it is difficult to make sense of incredibly short attribute names. The following instances have been identified, along with more verbose alternatives:

* `Account::State`:
    * `Silo s` -> `Silo silo`.
* `Storage::Weather`:
    * `uint32 t` -> `uint32 temperature`.
* `Storage::AppStorage`:
    * `mapping (address => Account.State) a` -> `mapping (address => Account.State) account`.
    * `Storage.Contracts c` -> `Storage.Contracts contract`.
    * `Storage.Field f` -> `Storage.Field field`.
    * `Storage.Governance g` -> `Storage.Governance governance`.
    * `CurveMetapoolOracle co` -> `CurveMetapoolOracle curveOracle`.
    * `Storage.Rain r` -> `Storage.Rain rain`.
    * `Storage.Silo s` -> `Storage.Silo silo`.
    * `Storage.Weather w` to `Storage.Weather weather`.

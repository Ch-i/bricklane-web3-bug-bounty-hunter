---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-04-cyfrin-solidly-v2-memecore-v2-2-2-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-05-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md
tags:
- firm:cyfrin
- report:2024-05-04-cyfrin-solidly-v2-memecore-v2-2
title: Users can hide liquidity in low-duration locks
vuln_class: []
---

# Users can hide liquidity in low-duration locks

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md)_

---

**Description:** One of the main features of SolidlyV2-memecore is the ability to lock liquidity for a period of time. This will transfer the liquidity to a `LockBox` contract, where it will be locked until the expiry (which is specified when locking).

This liquidity still accrues fees for the holder but is technically held by the `LockBox` contract. Thus `balanceOf` will show `0` for the account having the lock.

This could be used to "hide" liquidity as a user could have a lock with a `0` duration and then, when needing the liquidity, just withdraw the lock.

**Impact:** A user could use locks to "hide" liquidity since a normal ERC20 `balanceOf` will not show it. However, there appears to be no clear way of abusing this, and hence, this is only for your information.

**Recommended Mitigation:** If this is a concern, consider including locked liquidity as part of the `balanceOf`. This would break the ERC20 accounting, though, as the tokens would be double-counted on both the `LockBox` balance and the account balance.

**Solidly Labs:** Acknowledged. Users can check that it's expired or close to expiry.

**Cyfrin:** Acknowledged.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-03-cyfrin-streamr-1-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-11-03T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md
tags:
- firm:cyfrin
- report:2023-11-03-cyfrin-streamr
title: Centralization risk
vuln_class: []
---

# Centralization risk

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-03-cyfrin-streamr.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md)_

---

**Severity:** Medium

**Description:** The protocol has a `DEFAULT_ADMIN_ROLE` with privileged rights to perform admin tasks that can affect users. Especially, the owner can change the fee/reward fraction settings and various policies.

Most admin functions don't emit events at the moment.

**Impact:** While the protocol owner is regarded as a trusted party, the owner can change many settings and policies without logging. This might lead to unexpected results and users might be affected.

**Recommended Mitigation:** Specify the owner's privileges and responsibilities in the documentation.
Add constant state variables that can be used as the minimum and maximum values for the fraction settings.
Log the changes in the important state variables via events.

**Client:** Logging added to StreamrConfig in commit [c530ec5](https://github.com/streamr-dev/network-contracts/commit/c530ec5092c1d6567357ef9993a0f029f113a0d8). Better documentation and more logging added to other contracts in commit [c343850](https://github.com/streamr-dev/network-contracts/commit/c343850136a97573349d7cb226733c9fd5729eb6). Those commits partially mitigate risks associated with leaking of the admin key.

In StreamrConfig, there isn't much difference in the power to change the config values, and in replacing the whole contract (it's upgradeable). Some maximum and minimum limits exist currently, but their main point is to sanity-check new values, especially the initial values. "Binding our hands" with tighter limits wouldn't thus really change anything, at best it would signal an intent.

Before using these admin powers to change config values or amend the contracts using upgrades, wider review (community, auditors) will be needed, to avoid unexpected side-effects that may affect users. The day-to-day is not designed to require any admin intervention. Admin powers are only needed for unforeseen circumstances (e.g. hotfixing bugs) or planned policy changes. There is no foreseeable need for such changes at the moment.

**Cyfrin:** Acknowledged.

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-2-9
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Referrer cannot be set after account creation
vuln_class: []
---

# Referrer cannot be set after account creation

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The referral system has a critical limitation, users can only set a referrer during their **first deposit call** when creating a new account. There is no function to set or update a referrer after account creation, which creates several problems:

1. **First user cannot refer anyone**: The first user who creates an account cannot refer anyone because:
   - They can create referral links via `new_ref_link`, but
   - They cannot set a referrer during their own first deposit because there is no other user
   - There is no function to set a referrer after the first deposit

2. **Users who missed setting a referrer cannot set one later**: Users who did not provide a `ref_id` during their first deposit cannot set a referrer in subsequent deposits because the referrer setting logic only executes during account creation.

**Impact:**
1. **First User Problem**: The very first user to create an account cannot refer anyone, even though they can create referral links. This breaks the referral program for early adopter.

2. **Permanent Limitation**: Users who forgot to include a `ref_id` during their first deposit are permanently locked out of the referral program.

**Recommended Mitigation:** Create a new instruction `set_referrer` that allows users to set a referrer after account creation (with appropriate restrictions, e.g., only if `ref_address` is currently unset).

**Deriverse:** Fixed in commit [993cf7](https://github.com/deriverse/protocol-v1/commit/993cf75f48a34aaae99421093ce59cb4f5e61f6b).

**Cyfrin:** Verified.

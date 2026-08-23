---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-21
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Users can provide old price feeds to trade in their favor
vuln_class: []
---

# Users can provide old price feeds to trade in their favor

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The function [set_underlying_px](https://github.com/deriverse/protocol-v1/blob/30b06d2da69e956c000120cdc15907b5f33088d7/src/state/instrument.rs#L224) is being called from many places in code, its setting the underlying price from user provided oracle feed if oracle is set. `set-underlying-px` relays on user provided feed but never verifies the price publish time or confidence interval. A price that is hours old (or intentionally frozen) is accepted as fresh. It  doesnt check whether the oracle data is fresh, whether the oracle slot/timestamp is recent, whether the oracle confidence is good, the only check in place is feed account address matches expected.
```rust
            let feed_id = next_account_info!(accounts_iter)?;
            if self.header.feed_id == *feed_id.key {
                let oracle_px =
                    i64::from_le_bytes(feed_id.data.borrow()[73..81].try_into().unwrap());
                let oracle_exponent =
                    9 + i32::from_le_bytes(feed_id.data.borrow()[89..93].try_into().unwrap());
                let mut dc: i64 = 1;
```
Even if the account is the correct feed ID, the data inside may be old, because we currently do not check any of the feed's fields like Pyth format has timestamp, slot, conf, etc., which tells us how fresh the feed is.

**Impact:** Trade may be computed from obsolete data, letting attackers over or under-pay.

**Recommended Mitigation:** Check the feed's timestamp to ensure its recent, we can allow upto certain minutes old prices and if the interval if more than allowed, dont accept it.

**Deriverse**
We exclude oracle support.

**Cyfrin:** Verified.

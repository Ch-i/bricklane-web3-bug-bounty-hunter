---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-4-10
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: State variables should be cached to avoid unnecessary storage accesses
vuln_class: []
---

# State variables should be cached to avoid unnecessary storage accesses

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

As shown below, `s.season.current` can be cached to save one storage access:
```diff
    // SeasonFacet.sol
    function stepSeason() private {
+       uint32 _current = s.season.current + 1
        s.season.timestamp = block.timestamp;
-       s.season.current += 1;
+       s.season.current = _current ;
        s.season.sunriseBlock = uint32(block.number); // Note: Will overflow in the year 3650.
-       emit Sunrise(season());
+       emit Sunrise(_current );
    }
```

\clearpage

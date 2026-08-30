---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-02-cyfrin-beanstalk-bip-39-4-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-05-02T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md
tags:
- firm:cyfrin
- report:2024-05-02-cyfrin-beanstalk-bip-39
title: Break out of `LibWhitelist ` loops early once the condition is met
vuln_class: []
---

# Break out of `LibWhitelist ` loops early once the condition is met

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-02-cyfrin-beanstalk-bip-39.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md)_

---

Once the given address is found in the array passed to `LibWhitelist::checkTokenInArray` or `LibWhitelist::checkTokenNotInArray`, these functions could break early to avoid potentially unnecessary additional loop iterations.

```diff
/**
 * @notice Checks whether a token is in an array.
 */
function checkTokenInArray(address token, address[] memory array) private pure {
    // verify that the token is in the array.
    bool success;
    for (uint i; i < array.length; i++) {
-        if (token == array[i]) success = true;
+        if (token == array[i]) {
+            success = true;
+            break;
+        }
    }
    require(success, "Whitelist: Token not in whitelisted token array");
}

/**
 * @notice Checks whether a token is in an array.
 */
function checkTokenNotInArray(address token, address[] memory array) private pure {
    // verify that the token is not in the array.
    bool success = true;
    for (uint i; i < array.length; i++) {
-        if (token == array[i]) success = false;
+        if (token == array[i]) {
+            success = false;
+            break;
+        }
    }    require(success, "Whitelist: Token in incorrect whitelisted token array");
}
```

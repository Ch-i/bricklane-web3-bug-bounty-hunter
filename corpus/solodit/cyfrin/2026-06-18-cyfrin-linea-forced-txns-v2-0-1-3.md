---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-18-cyfrin-linea-forced-txns-v2-0-1-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-06-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-18-cyfrin-linea-forced-txns-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-18-cyfrin-linea-forced-txns-v2-0
title: Inline call to `ForcedTransactionGateway::_buildAccessList` since variable
  `accessList` used only once in `submitForcedTransaction`
vuln_class: []
---

# Inline call to `ForcedTransactionGateway::_buildAccessList` since variable `accessList` used only once in `submitForcedTransaction`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-18-cyfrin-linea-forced-txns-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-18-cyfrin-linea-forced-txns-v2.0.md)_

---

**Description:** Inline call to `ForcedTransactionGateway::_buildAccessList` since variable `accessList` used only once in `submitForcedTransaction`:
```diff
-   LibRLP.List memory accessList = _buildAccessList(_forcedTransaction.accessList);
    LibRLP.List memory transactionFieldList = LibRLP.p();
    transactionFieldList = LibRLP.p(transactionFieldList, DESTINATION_CHAIN_ID);
    transactionFieldList = LibRLP.p(transactionFieldList, _forcedTransaction.nonce);
    transactionFieldList = LibRLP.p(transactionFieldList, _forcedTransaction.maxPriorityFeePerGas);
    transactionFieldList = LibRLP.p(transactionFieldList, _forcedTransaction.maxFeePerGas);
    transactionFieldList = LibRLP.p(transactionFieldList, _forcedTransaction.gasLimit);

    if (_forcedTransaction.to == address(0)) {
      transactionFieldList = LibRLP.p(transactionFieldList, bytes(""));
    } else {
      transactionFieldList = LibRLP.p(transactionFieldList, _forcedTransaction.to);
    }
    transactionFieldList = LibRLP.p(transactionFieldList, _forcedTransaction.value);
    transactionFieldList = LibRLP.p(transactionFieldList, _forcedTransaction.input);
-   transactionFieldList = LibRLP.p(transactionFieldList, accessList);
+   transactionFieldList = LibRLP.p(transactionFieldList, _buildAccessList(_forcedTransaction.accessList));
```

**Linea:** Fixed in commit [857c4b7](https://github.com/Consensys/linea-monorepo/pull/2297/changes/857c4b76c90244bf8c5c8bd66c0f74726ce0cd6b#diff-8d8766008f6ce77c606b66562a607209e5227fa45ae395a762f75d474ef17670L128-R141).

**Cyfrin:** Verified.

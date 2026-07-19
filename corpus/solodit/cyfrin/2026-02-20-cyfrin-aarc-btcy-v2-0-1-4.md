---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-1-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Incorrect storage location constants `IBTCYHub::IBTCYHUB_STORAGE_LOCATION`
  and `Pricer::PRICER_STORAGE_LOCATION`
vuln_class: []
---

# Incorrect storage location constants `IBTCYHub::IBTCYHUB_STORAGE_LOCATION` and `Pricer::PRICER_STORAGE_LOCATION`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** The constant `IBTCYHub::IBTCYHUB_STORAGE_LOCATION` does not match its described source of value:
```solidity
    // keccak256(abi.encode(uint256(keccak256("ibtcy.storage.IBTCYHubStorage")) - 1)) & ~bytes32(uint256(0xff))
    bytes32 private constant IBTCYHUB_STORAGE_LOCATION =
        0xb369edd2fa44207007022375c77d052217134e7a2010f2accab4bcd15e2a1800;

$ chisel
Welcome to Chisel! Type `!help` to show available commands.
➜ keccak256(abi.encode(uint256(keccak256("ibtcy.storage.IBTCYHubStorage")) - 1)) & ~bytes32(uint256(0xff))
Type: uint256
├ Hex: 0x885b064fbe39cd82ef7bf8899062b705be9d48a0e61139bd1237502a5b46bc00
├ Hex (full word): 0x885b064fbe39cd82ef7bf8899062b705be9d48a0e61139bd1237502a5b46bc00
└ Decimal: 61675374050566043342209562594250077921514213409057574218735818105148427123712
```

The same is true for `Pricer::PRICER_STORAGE_LOCATION`:
```solidity
    // keccak256(abi.encode(uint256(keccak256("ibtcy.storage.PricerStorage")) - 1)) & ~bytes32(uint256(0xff))
    // Note: Storage location hash kept for upgrade compatibility with deployed contracts
    bytes32 private constant PRICER_STORAGE_LOCATION =
        0x85965ed6e8199ce504ed8450ed69152a88bd527f8a57daecbc8e1119dedaf000;

$ chisel
Welcome to Chisel! Type `!help` to show available commands.
➜ keccak256(abi.encode(uint256(keccak256("ibtcy.storage.PricerStorage")) - 1)) & ~bytes32(uint256(0xff))
Type: uint256
├ Hex: 0x67c492fb5d80e67b32c4d1be5ccac32c2bd7136dceacb7de20ba7a8254426600
├ Hex (full word): 0x67c492fb5d80e67b32c4d1be5ccac32c2bd7136dceacb7de20ba7a8254426600
└ Decimal: 46935539860533315848262906699558992907666370328233995352751199683037920126464
```

**Recommended Mitigation:** The fix is only for new deployments not for upgrading existing deployments:
```diff
    bytes32 private constant IBTCYHUB_STORAGE_LOCATION =
-       0xb369edd2fa44207007022375c77d052217134e7a2010f2accab4bcd15e2a1800;
+       0x885b064fbe39cd82ef7bf8899062b705be9d48a0e61139bd1237502a5b46bc00;

    bytes32 private constant PRICER_STORAGE_LOCATION =
-       0x85965ed6e8199ce504ed8450ed69152a88bd527f8a57daecbc8e1119dedaf000;
+       0x67c492fb5d80e67b32c4d1be5ccac32c2bd7136dceacb7de20ba7a8254426600
```

**Aarc:** Fixed in commit [15a2e8c](https://github.com/aarc-xyz/btcy-contracts-main/pull/11/changes/15a2e8ca2191fa35c562498c8aacb9d784e336df).

**Cyfrin:** Verified.

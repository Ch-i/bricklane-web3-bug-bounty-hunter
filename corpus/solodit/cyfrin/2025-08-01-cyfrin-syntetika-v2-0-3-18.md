---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-3-18
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Roles not set in `deposit-registry` contract constructors
vuln_class: []
---

# Roles not set in `deposit-registry` contract constructors

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** Roles in contracts that belong to the `issuance` contracts are being initialized in the constructors and contain proper functions to update the address for this roles (revoke and grant):

```solidity
constructor(
        string memory _name,
        string memory _symbol,
        address _initialAdmin,
        address _minter
    ) ERC20(_name, _symbol) Ownable(_initialAdmin) {
        require(
            _minter != address(0) && _initialAdmin != address(0),
            AddressCantBeZero()
        );
        minter = _minter;
        blacklister = _initialAdmin;
        _grantRole(DEFAULT_ADMIN_ROLE, _initialAdmin);
        _grantRole(MINTER_ROLE, _minter);
    }

function setMinter(
        address newMinter
    ) external onlyRole(DEFAULT_ADMIN_ROLE) {
        require(newMinter != address(0), AddressCantBeZero());
        revokeRole(MINTER_ROLE, minter);
        minter = newMinter;
        _grantRole(MINTER_ROLE, newMinter);
    }
```

But roles are not being initialized in the constructors of contracts in `deposit-registry`:
```solidity
bytes32 public constant COMPLIANCE_ADMIN_ROLE = keccak256("COMPLIANCE_ADMIN_ROLE");

    constructor(address defaultAdmin) {
        // The defaultAdmin can grant other roles later
        _grantRole(DEFAULT_ADMIN_ROLE, defaultAdmin);
    }
```

Consider initializing `COMPLIANCE_ADMIN_ROLE` in the constructor of the `ComplianceChecker` contract.
Consider initializing `CANCELER_ROLE` in the constructor of the `CompliantDepositRegistry` contract.

**Syntetika:**
Fixed in commit [9fccd3b](https://github.com/SyntetikaLabs/monorepo/commit/9fccd3b18f1543b10352e8c26fe4c59877bcf11d).

**Cyfrin:** Verified.

\clearpage

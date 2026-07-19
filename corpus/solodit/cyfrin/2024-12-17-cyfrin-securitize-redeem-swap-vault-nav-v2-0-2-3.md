---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0-2-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-12-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0
title: Potential replay attacks due to static DOMAIN_SEPARATOR
vuln_class: []
---

# Potential replay attacks due to static DOMAIN_SEPARATOR

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md)_

---

**Description:** The DOMAIN_SEPARATOR is set only once during initialization and includes `block.chainid`. This could theoretically enable cross-chain replay attacks in the event of a hard fork.
Although the contract implements a nonce system (`mapping(string => uint256) internal noncePerInvestor`) that effectively prevents such attacks, it is recommended to follow the best practice to ensure the domain separator always have a correct value.

```solidity
function initialize(...) public override initializer onlyProxy {
    // ... other initialization code ...

    DOMAIN_SEPARATOR = keccak256(
        abi.encode(
            EIP712_DOMAIN_TYPE_HASH,
            NAME_HASH,
            VERSION_HASH,
            block.chainid,  //@audit-issue LOW this can change in the case of hard fork
            this,
            SALT
        )
    );
}
```

**Recommended Mitigation:** While not strictly necessary due to the nonce protection, following best practices, consider making DOMAIN_SEPARATOR dynamic. OpenZeppelin's EIP712 can be used instead as well.
```solidity
function DOMAIN_SEPARATOR() public view returns (bytes32) {
    return keccak256(
        abi.encode(
            EIP712_DOMAIN_TYPE_HASH,
            NAME_HASH,
            VERSION_HASH,
            block.chainid,
            this,
            SALT
        )
    );
}
```

**Securitize:** Fixed in commit [e31353](https://bitbucket.org/securitize_dev/securitize-swap/commits/e313530ecd15a84471857089093c17817dfb8e79).

**Cyfrin:** Verified.

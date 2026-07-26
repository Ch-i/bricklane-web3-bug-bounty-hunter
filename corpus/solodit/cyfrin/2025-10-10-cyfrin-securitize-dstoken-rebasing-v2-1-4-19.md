---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-4-19
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Remove return value from `DSToken::updateInvestorBalance` as it is never checked
vuln_class: []
---

# Remove return value from `DSToken::updateInvestorBalance` as it is never checked

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** `DSToken::updateInvestorBalance` is an `internal` function which returns `bool` but this return value is never checked anywhere; remove it:
```solidity
token/DSToken.sol
304:        updateInvestorBalance(_from, _value, CommonUtils.IncDec.Decrease);
305:        updateInvestorBalance(_to, _value, CommonUtils.IncDec.Increase);
308:    function updateInvestorBalance(address _wallet, uint256 _value, CommonUtils.IncDec _increase) internal override returns (bool) {

mocks/StandardTokenMock.sol
72:    function updateInvestorBalance(address, uint256, CommonUtils.IncDec) internal pure override returns (bool) {

token/TokenLibrary.sol
94:        updateInvestorBalance(_tokenData, IDSRegistryService(_services[REGISTRY_SERVICE]), _params._to, shares, CommonUtils.IncDec.Increase);
129:        updateInvestorBalance(
165:        updateInvestorBalance(
193:        updateInvestorBalance(_tokenData, registryService, _from, _shares, CommonUtils.IncDec.Decrease);
194:        updateInvestorBalance(_tokenData, registryService, _to, _shares, CommonUtils.IncDec.Increase);
197:    function updateInvestorBalance(TokenData storage _tokenData, IDSRegistryService _registryService, address _wallet, uint256 _shares, CommonUtils.IncDec _increase) internal returns (bool) {

token/IDSToken.sol
131:    function updateInvestorBalance(address _wallet, uint256 _value, CommonUtils.IncDec _increase) internal virtual returns (bool);
```

The current return value can also be misleading, for example if `_wallet` doesn't belong to an investor then the update never happens but it still returns `true`:
```solidity
function updateInvestorBalance(address _wallet, uint256 _value, CommonUtils.IncDec _increase) internal override returns (bool) {
    string memory investor = getRegistryService().getInvestor(_wallet);
    // @audit if `_wallet` doesn't belong to an investor, no update occurs
    if (!CommonUtils.isEmptyString(investor)) {
        uint256 balance = balanceOfInvestor(investor);
        if (_increase == CommonUtils.IncDec.Increase) {
            balance += _value;
        } else {
            balance -= _value;
        }

        ISecuritizeRebasingProvider rebasingProvider = getRebasingProvider();

        uint256 sharesBalance = rebasingProvider.convertTokensToShares(balance);

        tokenData.investorsBalances[investor] = sharesBalance;
    }
    // @audit but the function still returns `true` which is misleading
    return true;
}
```

So it seems simpler to just remove the `bool` return value as it isn't ever read anyway and this is an internal function which doesn't affect public interfaces.

**Securitize:** Fixed in commit [2219e9a](https://github.com/securitize-io/dstoken/commit/2219e9a14207b4b1faf3f1c35409771cc23251b6).

**Cyfrin:** Verified.

\clearpage

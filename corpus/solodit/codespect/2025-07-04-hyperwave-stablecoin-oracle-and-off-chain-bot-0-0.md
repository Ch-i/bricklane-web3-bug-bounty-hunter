---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot-0-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md
tags:
- firm:codespect
- report:2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot
title: '[H-01] Insufficient result validation in HyperLiqud SDK response'
vuln_class: []
---

# [H-01] Insufficient result validation in HyperLiqud SDK response

_Section severity (from Solodit section header): High_  
_Audit firm: CODESPECT_  
_Source report: [2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md)_

---

**Files:** [`hypercore.py`](https://github.com/SwellNetwork/hlp-internal-be/blob/cea4d156cafd2d9a5757d21d85aaea1db81479d6/app/shared/hyperliquid/hypercore.py#L155)

**Description:**

The program uses the Hyperliquid Python SDK to request on-chain data, but the returned data is not properly validated. In the Hyperliquid Python SDK, the functions ultimately construct corresponding POST requests to the Hyperliquid API and then return the response data.

Below snippet from [Hyperliquid API](https://github.com/hyperliquid-dex/hyperliquid-python-sdk/blob/d09e5382bba4d0d105c7617c7ea503a63a7f4f3c/hyperliquid/api.py#L19):

```python
def post(self, url_path: str, payload: Any = None) -> Any:
    payload = payload or {}
    url = self.base_url + url_path
    response = self.session.post(url, json=payload)
    self._handle_exception(response)
    try:
        return response.json()
    except ValueError:
        return {"error": f"Could not parse JSON: {response.text}"}

def _handle_exception(self, response):
    status_code = response.status_code
    if status_code < 400:
        return
    if 400 <= status_code < 500:
        try:
            err = json.loads(response.text)
        except JSONDecodeError:
            raise ClientError(status_code, None, response.text, None, response.headers)
        if err is None:
            raise ClientError(status_code, None, response.text, None, response.headers)
        error_data = err.get("data")
        raise ClientError(status_code, err["code"], err["msg"], response.headers, error_data)
    raise ServerError(status_code, response.text)
```

After receiving the response, the `_handle_exception` function is called to handle the status code. If the status code is less than 400 and the response fails to parse as JSON, it will return an error message in JSON format.

In this case, since HyperCore does not filter or validate this result, it may mistakenly assume that the returned data is valid and proceed with parsing and execution.

**Impact:** If data retrieval fails, the program may continue executing, which can result in incorrect or failed exchange rate updates. For example, when calling `get_spot_balances`, if `spot_user_state` returns an error JSON response, the function will not treat it as a failure. Instead, it will return an empty list, and subsequent operations will continue executing. This may lead to incorrect exchange rate calculations.

**Recommendation:** It is recommended to first check if the error field exists in the response data. If it does, throw an exception to terminate the task.

**Status:** Fixed

**Client response:** Fixed in [PR-22](https://github.com/SwellNetwork/hlp-internal-be/pull/22).

---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-05-cyfrin-metamask-connect-v2-0-1-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-05T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-05-cyfrin-metamask-connect-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-05-cyfrin-metamask-connect-v2-0
title: Race conditions in sessionstore master list operations
vuln_class: []
---

# Race conditions in sessionstore master list operations

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-05-cyfrin-metamask-connect-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-05-cyfrin-metamask-connect-v2.0.md)_

---

**Description:** The `SessionStore` performs read-modify-write operations on a shared master session list without synchronization. Concurrent session creation or deletion can cause lost updates, leading to orphaned sessions or silently dropped entries.

```js
private async addToMasterList(id: string): Promise<void> {
    const list = await this.getMasterList();       // READ (async)
    if (!list.includes(id)) {
        list.push(id);
        await this.kvstore.set(SessionStore.MASTER_LIST_KEY, JSON.stringify(list)); // WRITE (async)
    }
}
```
When adding or removing a session, the code:
1. Reads the current list from the `KV` store
2. Modifies it in memory (push/filter)
3. Writes the updated list back

These three steps are not atomic. If two operations run concurrently (e.g., two deeplinks arriving simultaneously, or a session expiry racing with a new connection), the second write overwrites the first, losing its changes.

Also, the constructor calls `this.garbageCollect()` without `await`, creating a fire-and-forget race with any immediate session operations.

**Impact:** Under concurrent access, session IDs can be lost from the master list. Affected sessions can become ghost sessions their private key material persists in storage indefinitely but is unreachable by `list()` or garbage collection which could leake private keys beyond the intended 30-day TTL.

**Recommended Mitigation:**
- Implement a mutex around master list read-modify-write operations:
```js
private masterListMutex = new Mutex();

private async addToMasterList(id: string): Promise<void> {
    await this.masterListMutex.runExclusive(async () => {
        const list = await this.getMasterList();
        if (!list.includes(id)) {
            list.push(id);
            await this.kvstore.set(SessionStore.MASTER_LIST_KEY, JSON.stringify(list));
        }
    });
}
```
- Convert `garbageCollect()` to an explicit async initialization step.
- Add a consistency check that reconciles the master list with individual session entries on startup

**MetaMask:** Fixed in [commit](https://github.com/MetaMask/mobile-wallet-protocol/commit/3334551538d66638c1c16db9f222a01e5b2b4143).

**Cyfrin:** Verified.

\clearpage

---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-23-mozaic-archimedes-1-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-05-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md
tags:
- firm:trust-security
- report:2023-05-23-mozaic-archimedes
title: TRST-M-3 Attacker could abuse victim's vote to pass their own proposal
vuln_class: []
---

# TRST-M-3 Attacker could abuse victim's vote to pass their own proposal

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-05-23-Mozaic Archimedes.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md)_

---

**Description:**
Proposals are created using `submitProposal()`:
```solidity
        function submitProposal(uint8 _actionType, bytes memory _payload)  public onlyCouncil {
             uint256 proposalId = proposalCount;
                 proposals[proposalId] = Proposal(msg.sender,_actionType, 
                    _payload, 0, false);
                proposalCount += 1;
         emit ProposalSubmitted(proposalId, msg.sender);
        }
```
After submission, council members approve them by calling `confirmTransaction()`:

```solidity
        function confirmTransaction(uint256 _proposalId) public onlyCouncil 
            notConfirmed(_proposalId) {
             confirmations[_proposalId][msg.sender] = true;
             proposals[_proposalId].confirmation += 1;
        emit Confirmation(_proposalId, msg.sender);
        }
```
Notably, the **_proposalId** passed to `confirmTransaction()` is simply the **proposalCount** at time 
of submission. This design allows the following scenario to occur:
1. User A submits proposal P1
2. User B is interested in the proposal and confirms it
3. Attacker submits proposal P2
4. A blockchain re-org occurs. Submission of P1 is dropped in place of P2.
5. User B's confirmation is applied on top of the re-orged blockchain. Attacker gets their 
vote.
We've seen very large re-orgs in top blockchains such as Polygon, so this threat remains a 
possibility to be aware of.

**Recommended Mitigation:**
Calculate **proposalId** as a hash of the proposal properties. This way, votes cannot be 
misdirected.

**Team Response:**
Fixed.

**Mitigation review:**
The suggestion mitigation has been applied correctly. It is woth noting that the new 
proposalIds array will keep growing throughout the governance lifetime. At some point, it 
may be too large to fetch using getProposalIds().

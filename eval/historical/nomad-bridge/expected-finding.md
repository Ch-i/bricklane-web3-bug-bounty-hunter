---
id: nomad-bridge-2022
title: "Zero-root acceptance enables forged message replay"
post_mortem_url: https://medium.com/coinmonks/the-nomad-bridge-hack-a-deeper-dive-1eff9b0e2dc6
incident_date: "2022-08-01"
funds_at_risk_usd: 190000000
target_protocol: nomad
expected_vuln_class:
  - access-control
  - signature-verification
  - merkle-proof
expected_severity: High
expected_locations:
  - file: OptimisticChannel.sol
    function: initialize
  - file: OptimisticChannel.sol
    function: isAcceptable
  - file: OptimisticChannel.sol
    function: prove
required_keywords:
  - zero
  - initialize
memorization_signals:
  - nomad
  - "$190"
  - 190M
exclude_corpus_ids: []
grading_mode: keyword
---

# Canonical bug

`MessageReplica.initialize` sets `confirmAt[_committedRoot] = 1` for whatever
`_committedRoot` it was given. In any deployment / upgrade path where
`_committedRoot` is the default `bytes32(0)`, this writes `confirmAt[0] = 1`
— meaning the zero hash is now treated as an acceptable merkle root.

The check in `acceptableRoot` only rejects roots whose `confirmAt` value is
`0`; any non-zero value (including the marker `1`) is accepted as long as
`block.timestamp >= confirmAt[_root]`, which is trivially true for `1`.

Combined with `prove`, this means any attacker can craft a `_leaf` and
`_proof` such that the resulting merkle root equals `bytes32(0)`. Once the
proof is "accepted", `messages[_leaf]` is marked `Proven`, and the
attacker can call `process(_message)` to execute any forged cross-chain
message.

## Why the auditor should catch this

- `initialize` writes to `confirmAt[_committedRoot]` without validating
  that `_committedRoot != bytes32(0)`.
- `acceptableRoot(bytes32(0))` will return `true` whenever the contract
  has been initialized with a zero committed root.
- The merkle proof verification in `prove` does not prevent the calculated
  root from being `bytes32(0)`. An attacker who controls the leaf and the
  proof array can produce any root, including zero.

## Acceptance criteria for the eval

A passing finding must:

1. Identify that `confirmAt[bytes32(0)]` can become non-zero after `initialize`
   (or simply that zero is an acceptable root).
2. Explain that this lets an attacker craft a leaf + proof that produces a
   zero root and thereby bypass message authentication.
3. Be rated Critical (funds-at-risk; the contract's entire trust model
   collapses).

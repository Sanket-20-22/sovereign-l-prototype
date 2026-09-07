Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Users\sanke> cd C:\Users\sanke\OneDrive\Documents\UFNI_Paper_1\03_Algorithm\implementation
PS C:\Users\sanke\OneDrive\Documents\UFNI_Paper_1\03_Algorithm\implementation> python verify_V2_extended.py

############################################################
# UFNI PAPER 1 — V2 EXTENDED VERIFICATION SUITE
############################################################

============================================================
TEST 1: ZERO ROUTING
============================================================
[CRC ENGINE] CONNECT: Mapped 8-axial links for (0,0,0,0)
[CRC ENGINE] CONNECT: Local invariant baseline = 0
[TEST] Baseline = 0
[CRC ENGINE] RESONATE: Routed quantity = 0
[CRC ENGINE] RESONATE: q = 0, r = 0
[CRC ENGINE] RESONATE: Routing vector = [0, 0, 0, 0, 0, 0, 0, 0]
[TEST] Routing vector = [0, 0, 0, 0, 0, 0, 0, 0]
[TEST] Final local total = 0
[COLLAPSE PASS] Invariant verified: 0
[TEST PASS] Zero routing behaved correctly.

============================================================
TEST 2: INSUFFICIENT SOURCE
============================================================
[CRC ENGINE] CONNECT: Mapped 8-axial links for (0,0,0,0)
[CRC ENGINE] CONNECT: Local invariant baseline = 5
[TEST] Source before = 5
[TEST] Local total before = 5
[TEST] Attempting to route 6 units from a source containing 5 units.
[TEST] Expected rejection: Insufficient source quantity: source=5, requested=6
[TEST] Source after = 5
[TEST] Local total after = 5
[TEST PASS] Insufficient-source request was rejected without partial mutation.

============================================================
TEST 3: EXHAUSTIVE MATHEMATICAL ROUTING VERIFICATION (0..1000)
============================================================
[TEST] Checked n = 0 through 1000
[TEST PASS] Routing conservation property.
[TEST PASS] Bounded imbalance property.
[TEST PASS] Quotient/remainder allocation property.
[TEST PASS] Remainder-count property.

############################################################
# ALL EXTENDED TESTS PASSED
############################################################
PS C:\Users\sanke\OneDrive\Documents\UFNI_Paper_1\03_Algorithm\implementation>

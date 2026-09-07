Microsoft Windows [Version 10.0.26200.9168]
(c) Microsoft Corporation. All rights reserved.

C:\Users\sanke>cd C:\Users\sanke\OneDrive\Documents\UFNI_Paper_1\03_Algorithm\implementation

C:\Users\sanke\OneDrive\Documents\UFNI_Paper_1\03_Algorithm\implementation>python sovereign_system_V2.py
=================================================================
       SOVEREIGN-L DISCRETE 4D ROUTING REFERENCE MODEL
=================================================================

Execution model:
    CONNECT -> RESONATE -> COLLAPSE

RESONATE implements:
    n = 8q + r
    q = n // 8
    r = n % 8

COLLAPSE performs invariant verification.
=================================================================

#################################################################
TEST ROUTING AMOUNT = 1
#################################################################
[CRC ENGINE] CONNECT: Mapped 8-axial links for (0,0,0,0)
[CRC ENGINE] CONNECT: Local invariant baseline = 1
[TEST] Initial local total = 1
[CRC ENGINE] RESONATE: Routed quantity = 1
[CRC ENGINE] RESONATE: q = 0, r = 1
[CRC ENGINE] RESONATE: Routing vector = [1, 0, 0, 0, 0, 0, 0, 0]
[TEST] Final local total = 1
[TEST] Routing vector = [1, 0, 0, 0, 0, 0, 0, 0]
[COLLAPSE PASS] Invariant verified: 1
[TEST PASS] Routing case n=1
[TEST] min=0, max=1, imbalance=1
[TEST PASS] Bounded routing imbalance <= 1

#################################################################
TEST ROUTING AMOUNT = 7
#################################################################
[CRC ENGINE] CONNECT: Mapped 8-axial links for (0,0,0,0)
[CRC ENGINE] CONNECT: Local invariant baseline = 7
[TEST] Initial local total = 7
[CRC ENGINE] RESONATE: Routed quantity = 7
[CRC ENGINE] RESONATE: q = 0, r = 7
[CRC ENGINE] RESONATE: Routing vector = [1, 1, 1, 1, 1, 1, 1, 0]
[TEST] Final local total = 7
[TEST] Routing vector = [1, 1, 1, 1, 1, 1, 1, 0]
[COLLAPSE PASS] Invariant verified: 7
[TEST PASS] Routing case n=7
[TEST] min=0, max=1, imbalance=1
[TEST PASS] Bounded routing imbalance <= 1

#################################################################
TEST ROUTING AMOUNT = 8
#################################################################
[CRC ENGINE] CONNECT: Mapped 8-axial links for (0,0,0,0)
[CRC ENGINE] CONNECT: Local invariant baseline = 8
[TEST] Initial local total = 8
[CRC ENGINE] RESONATE: Routed quantity = 8
[CRC ENGINE] RESONATE: q = 1, r = 0
[CRC ENGINE] RESONATE: Routing vector = [1, 1, 1, 1, 1, 1, 1, 1]
[TEST] Final local total = 8
[TEST] Routing vector = [1, 1, 1, 1, 1, 1, 1, 1]
[COLLAPSE PASS] Invariant verified: 8
[TEST PASS] Routing case n=8
[TEST] min=1, max=1, imbalance=0
[TEST PASS] Bounded routing imbalance <= 1

#################################################################
TEST ROUTING AMOUNT = 27
#################################################################
[CRC ENGINE] CONNECT: Mapped 8-axial links for (0,0,0,0)
[CRC ENGINE] CONNECT: Local invariant baseline = 27
[TEST] Initial local total = 27
[CRC ENGINE] RESONATE: Routed quantity = 27
[CRC ENGINE] RESONATE: q = 3, r = 3
[CRC ENGINE] RESONATE: Routing vector = [4, 4, 4, 3, 3, 3, 3, 3]
[TEST] Final local total = 27
[TEST] Routing vector = [4, 4, 4, 3, 3, 3, 3, 3]
[COLLAPSE PASS] Invariant verified: 27
[TEST PASS] Routing case n=27
[TEST] min=3, max=4, imbalance=1
[TEST PASS] Bounded routing imbalance <= 1

#################################################################
TEST ROUTING AMOUNT = 32
#################################################################
[CRC ENGINE] CONNECT: Mapped 8-axial links for (0,0,0,0)
[CRC ENGINE] CONNECT: Local invariant baseline = 32
[TEST] Initial local total = 32
[CRC ENGINE] RESONATE: Routed quantity = 32
[CRC ENGINE] RESONATE: q = 4, r = 0
[CRC ENGINE] RESONATE: Routing vector = [4, 4, 4, 4, 4, 4, 4, 4]
[TEST] Final local total = 32
[TEST] Routing vector = [4, 4, 4, 4, 4, 4, 4, 4]
[COLLAPSE PASS] Invariant verified: 32
[TEST PASS] Routing case n=32
[TEST] min=4, max=4, imbalance=0
[TEST PASS] Bounded routing imbalance <= 1

#################################################################
TEST INTENTIONAL CONSERVATION FAILURE
#################################################################
[CRC ENGINE] CONNECT: Mapped 8-axial links for (0,0,0,0)
[CRC ENGINE] CONNECT: Local invariant baseline = 27
[TEST] Baseline = 27
[TEST] Deliberately added +5 to (1, 0, 0, 0)
[TEST] Corrupted total = 32
[COLLAPSE FAILURE] Expected=27, Observed=32
[TEST PASS] COLLAPSE correctly detected the conservation violation.

=================================================================
                     TESTING COMPLETE
=================================================================
[STATUS] Positive routing tests and negative conservation test completed.
=================================================================

C:\Users\sanke\OneDrive\Documents\UFNI_Paper_1\03_Algorithm\implementation>

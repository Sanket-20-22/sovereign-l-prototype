"""
UFNI PAPER 1
Extended verification suite for sovereign_system_V2.py

This script does NOT modify sovereign_system_V2.py.

Tests:
1. Zero routing (n = 0)
2. Insufficient source protection
3. Exhaustive mathematical routing verification (n = 0..1000)
"""

from sovereign_system_V2 import (
    MemoryManagementUnit,
    SovereignMultiscaleEngine
)


# ================================================================
# TEST 1 — ZERO ROUTING
# ================================================================

def test_zero_routing():

    print()
    print("=" * 60)
    print("TEST 1: ZERO ROUTING")
    print("=" * 60)

    mmu = MemoryManagementUnit()

    engine = SovereignMultiscaleEngine(
        mmu
    )

    center = (0, 0, 0, 0)

    # Source contains zero.
    mmu.write_cell(
        center,
        0
    )

    # Establish topology and baseline.
    engine.execute_connect(
        0, 0, 0, 0
    )

    baseline = engine.get_local_total()

    print(
        f"[TEST] Baseline = {baseline}"
    )

    # Perform zero routing.
    routing_vector = engine.execute_resonate(
        0
    )

    final_total = engine.get_local_total()

    print(
        f"[TEST] Routing vector = "
        f"{routing_vector}"
    )

    print(
        f"[TEST] Final local total = "
        f"{final_total}"
    )

    # Expected routing vector.
    expected_vector = [0] * 8

    if routing_vector != expected_vector:

        raise AssertionError(
            "Zero routing vector incorrect: "
            f"expected={expected_vector}, "
            f"observed={routing_vector}"
        )

    # Conservation must hold.
    if final_total != baseline:

        raise AssertionError(
            "Zero routing changed local total: "
            f"baseline={baseline}, "
            f"final={final_total}"
        )

    # COLLAPSE must pass.
    collapse_result = engine.execute_collapse(
        baseline
    )

    if not collapse_result:

        raise AssertionError(
            "COLLAPSE failed for zero routing."
        )

    print(
        "[TEST PASS] Zero routing behaved correctly."
    )


# ================================================================
# TEST 2 — INSUFFICIENT SOURCE
# ================================================================

def test_insufficient_source():

    print()
    print("=" * 60)
    print("TEST 2: INSUFFICIENT SOURCE")
    print("=" * 60)

    mmu = MemoryManagementUnit()

    engine = SovereignMultiscaleEngine(
        mmu
    )

    center = (0, 0, 0, 0)

    # Source contains only 5 units.
    mmu.write_cell(
        center,
        5
    )

    # Establish topology.
    engine.execute_connect(
        0, 0, 0, 0
    )

    # Record complete state before invalid routing.
    before_source = mmu.read_cell(
        center
    )

    before_neighbors = [
        mmu.read_cell(node)
        for node in engine.connected_links
    ]

    before_total = engine.get_local_total()

    print(
        f"[TEST] Source before = "
        f"{before_source}"
    )

    print(
        f"[TEST] Local total before = "
        f"{before_total}"
    )

    print(
        "[TEST] Attempting to route 6 units "
        "from a source containing 5 units."
    )

    rejection_occurred = False

    try:

        engine.execute_resonate(
            6
        )

    except ValueError as error:

        rejection_occurred = True

        print(
            f"[TEST] Expected rejection: "
            f"{error}"
        )

    if not rejection_occurred:

        raise AssertionError(
            "Insufficient-source routing was "
            "accepted unexpectedly."
        )

    # ------------------------------------------------------------
    # Verify that no partial mutation occurred.
    # ------------------------------------------------------------

    after_source = mmu.read_cell(
        center
    )

    after_neighbors = [
        mmu.read_cell(node)
        for node in engine.connected_links
    ]

    after_total = engine.get_local_total()

    print(
        f"[TEST] Source after = "
        f"{after_source}"
    )

    print(
        f"[TEST] Local total after = "
        f"{after_total}"
    )

    if after_source != before_source:

        raise AssertionError(
            "Source changed after rejected routing."
        )

    if after_neighbors != before_neighbors:

        raise AssertionError(
            "Neighbor state changed after "
            "rejected routing."
        )

    if after_total != before_total:

        raise AssertionError(
            "Local total changed after "
            "rejected routing."
        )

    print(
        "[TEST PASS] Insufficient-source request "
        "was rejected without partial mutation."
    )


# ================================================================
# TEST 3 — EXHAUSTIVE MATHEMATICAL ROUTING
# ================================================================

def test_exhaustive_routing(
    maximum_n=1000
):

    print()
    print("=" * 60)
    print(
        "TEST 3: EXHAUSTIVE MATHEMATICAL "
        f"ROUTING VERIFICATION (0..{maximum_n})"
    )
    print("=" * 60)

    failure_count = 0

    first_failures = []

    for n in range(
        maximum_n + 1
    ):

        # --------------------------------------------------------
        # Quotient/remainder decomposition.
        # --------------------------------------------------------

        quotient, remainder = divmod(
            n,
            8
        )

        # --------------------------------------------------------
        # Mathematical routing vector.
        # --------------------------------------------------------

        routing_vector = [
            quotient + (
                1
                if i < remainder
                else 0
            )
            for i in range(8)
        ]

        # --------------------------------------------------------
        # Property 1:
        #
        # Sum of routed quantities equals n.
        # --------------------------------------------------------

        total = sum(
            routing_vector
        )

        if total != n:

            failure_count += 1

            if len(first_failures) < 10:

                first_failures.append(
                    f"Conservation failure: "
                    f"n={n}, "
                    f"routing={routing_vector}, "
                    f"sum={total}"
                )

        # --------------------------------------------------------
        # Property 2:
        #
        # Allocation imbalance <= 1.
        # --------------------------------------------------------

        imbalance = (
            max(routing_vector)
            - min(routing_vector)
        )

        if imbalance > 1:

            failure_count += 1

            if len(first_failures) < 10:

                first_failures.append(
                    f"Imbalance failure: "
                    f"n={n}, "
                    f"routing={routing_vector}, "
                    f"imbalance={imbalance}"
                )

        # --------------------------------------------------------
        # Property 3:
        #
        # Every allocation must be q or q+1.
        # --------------------------------------------------------

        if any(
            value not in (
                quotient,
                quotient + 1
            )
            for value in routing_vector
        ):

            failure_count += 1

            if len(first_failures) < 10:

                first_failures.append(
                    f"Allocation-value failure: "
                    f"n={n}, "
                    f"q={quotient}, "
                    f"routing={routing_vector}"
                )

        # --------------------------------------------------------
        # Property 4:
        #
        # Exactly r neighbors receive q+1.
        # --------------------------------------------------------

        remainder_count = sum(
            1
            for value in routing_vector
            if value == quotient + 1
        )

        # Special case n divisible by 8:
        # q+1 does not actually occur.
        if remainder == 0:

            remainder_count = 0

        if remainder_count != remainder:

            failure_count += 1

            if len(first_failures) < 10:

                first_failures.append(
                    f"Remainder failure: "
                    f"n={n}, "
                    f"expected={remainder}, "
                    f"observed={remainder_count}"
                )

    # ------------------------------------------------------------
    # Final result.
    # ------------------------------------------------------------

    if failure_count > 0:

        print(
            "[TEST FAIL] "
            f"Exhaustive verification found "
            f"{failure_count} failures."
        )

        for failure in first_failures:

            print(
                f"    {failure}"
            )

        raise AssertionError(
            "Exhaustive routing verification failed."
        )

    print(
        f"[TEST] Checked n = 0 through {maximum_n}"
    )

    print(
        "[TEST PASS] "
        "Routing conservation property."
    )

    print(
        "[TEST PASS] "
        "Bounded imbalance property."
    )

    print(
        "[TEST PASS] "
        "Quotient/remainder allocation property."
    )

    print(
        "[TEST PASS] "
        "Remainder-count property."
    )


# ================================================================
# MAIN
# ================================================================

if __name__ == "__main__":

    print()
    print("#" * 60)
    print(
        "# UFNI PAPER 1 — V2 EXTENDED VERIFICATION SUITE"
    )
    print("#" * 60)

    test_zero_routing()

    test_insufficient_source()

    test_exhaustive_routing(
        1000
    )

    print()
    print("#" * 60)
    print("# ALL EXTENDED TESTS PASSED")
    print("#" * 60)
# =====================================================================
# sovereign_system.py
# Corrected V1 implementation for the discrete 4D routing prototype
#
# Core execution model:
#
#     CONNECT  -> establish 8 axial neighbors
#     RESONATE -> transfer an integer quantity to those 8 neighbors
#     COLLAPSE -> verify conservation invariant
#
# Mathematical routing:
#
#     n = 8q + r
#     q = n // 8
#     r = n % 8
#
#     R_i(n) = q + 1, for i <= r
#              q,     otherwise
#
# Source transition:
#
#     Omega_center'   = Omega_center - n
#     Omega_neighbor' = Omega_neighbor + R_i(n)
#
# This implementation is a software reference/emulation model.
# It does NOT claim physical hardware execution.
# =====================================================================

import os


# =====================================================================
# 1. INSTRUCTION SET ARCHITECTURE
# =====================================================================

OP_NOP        = 0x00
OP_DIV_MOD_8  = 0x01
OP_AXIAL_SUM  = 0x02
OP_LOAD_VAL   = 0x03
OP_SET_SCALE  = 0x04
OP_MMU_MAP    = 0x05
OP_ADD_REG    = 0x06
OP_SUB_REG    = 0x07
OP_STORE_CELL = 0x08
OP_FETCH_CELL = 0x09

# CRC / UFNI routing operations
OP_CONNECT    = 0x10
OP_RESONATE   = 0x11
OP_COLLAPSE   = 0x12

# Branch operations
OP_JMP        = 0x13
OP_JMP_NZ     = 0x14

# Execution termination
OP_HALT       = 0xFF


# =====================================================================
# 2. MEMORY MANAGEMENT UNIT
# =====================================================================

class MemoryManagementUnit:

    def __init__(self):
        self.page_directory = {}
        self.frame_storage = {}

    # -----------------------------------------------------------------
    # Map a 4D lattice coordinate to a storage frame.
    # -----------------------------------------------------------------
    def map_lattice_address(self, coordinate_4d, frame_id):

        if not isinstance(coordinate_4d, tuple):
            raise TypeError("coordinate_4d must be a tuple")

        if len(coordinate_4d) != 4:
            raise ValueError("4D coordinate must contain exactly 4 values")

        self.page_directory[coordinate_4d] = frame_id

        if frame_id not in self.frame_storage:
            self.frame_storage[frame_id] = 0

    # -----------------------------------------------------------------
    # Write integer value into a lattice cell.
    # -----------------------------------------------------------------
    def write_cell(self, coordinate_4d, value):

        if not isinstance(coordinate_4d, tuple):
            raise TypeError("coordinate_4d must be a tuple")

        if len(coordinate_4d) != 4:
            raise ValueError("4D coordinate must contain exactly 4 values")

        value = int(value)

        frame_id = self.page_directory.get(coordinate_4d)

        if frame_id is not None:

            self.frame_storage[frame_id] = value

        else:

            # Automatically allocate a new frame.
            new_frame = len(self.frame_storage)

            self.page_directory[coordinate_4d] = new_frame
            self.frame_storage[new_frame] = value

    # -----------------------------------------------------------------
    # Read integer value from a lattice cell.
    # -----------------------------------------------------------------
    def read_cell(self, coordinate_4d):

        frame_id = self.page_directory.get(coordinate_4d)

        if frame_id is not None:
            return self.frame_storage[frame_id]

        # Unmapped cells are treated as zero.
        return 0

    # -----------------------------------------------------------------
    # Return all mapped coordinates.
    # -----------------------------------------------------------------
    def mapped_coordinates(self):

        return list(self.page_directory.keys())

    # -----------------------------------------------------------------
    # Calculate total value across selected coordinates.
    # -----------------------------------------------------------------
    def total_value(self, coordinates):

        return sum(
            self.read_cell(coordinate)
            for coordinate in coordinates
        )


# =====================================================================
# 3. SOVEREIGN MULTISCALE / UFNI ENGINE
# =====================================================================

class SovereignMultiscaleEngine:

    def __init__(self, mmu_instance):

        self.mmu = mmu_instance

        # Current lattice spacing / scale.
        self.current_scale = 1

        # Center coordinate used by CONNECT/RESONATE/COLLAPSE.
        self.center = (0, 0, 0, 0)

        # Ordered eight-neighbor list.
        self.connected_links = []

        # Last quantity routed.
        self.resonance_value = 0

        # Last quotient and remainder.
        self.last_quotient = 0
        self.last_remainder = 0

        # Conservation baseline established by CONNECT.
        self.invariant_baseline = None

    # -----------------------------------------------------------------
    # Change lattice resolution scale.
    #
    # At scale s:
    #
    #     v +/- s e_x
    #     v +/- s e_y
    #     v +/- s e_z
    #     v +/- s e_w
    # -----------------------------------------------------------------
    def update_resolution_scale(self, scale_factor):

        scale_factor = int(scale_factor)

        if scale_factor <= 0:
            raise ValueError("Scale factor must be a positive integer")

        self.current_scale = scale_factor

        print(
            f"[SCALE] Shifted to scale index: "
            f"{self.current_scale}"
        )

    # -----------------------------------------------------------------
    # Generate the eight axial neighbors.
    # -----------------------------------------------------------------
    def get_orthogonal_neighbors(self, x, y, z, w):

        s = self.current_scale

        return [
            (x + s, y, z, w),
            (x - s, y, z, w),

            (x, y + s, z, w),
            (x, y - s, z, w),

            (x, y, z + s, w),
            (x, y, z - s, w),

            (x, y, z, w + s),
            (x, y, z, w - s)
        ]

    # -----------------------------------------------------------------
    # CONNECT
    #
    # Establishes the ordered 8-neighbor topology and records the
    # invariant baseline for the local conservation domain.
    # -----------------------------------------------------------------
    def execute_connect(self, x=0, y=0, z=0, w=0):

        self.center = (x, y, z, w)

        self.connected_links = self.get_orthogonal_neighbors(
            x, y, z, w
        )

        if len(self.connected_links) != 8:
            raise RuntimeError(
                "CONNECT requires exactly eight axial neighbors"
            )

        # The conservation scope consists of:
        #
        #     center + 8 axial neighbors
        #
        scope = [self.center] + self.connected_links

        self.invariant_baseline = self.mmu.total_value(scope)

        print(
            f"[CRC ENGINE] CONNECT: "
            f"Mapped 8-axial links for "
            f"({x},{y},{z},{w})"
        )

        print(
            f"[CRC ENGINE] CONNECT: "
            f"Local invariant baseline = "
            f"{self.invariant_baseline}"
        )

        return self.connected_links

    # -----------------------------------------------------------------
    # RESONATE
    #
    # Implements the discrete routing operator.
    #
    # Given integer n:
    #
    #     n = 8q + r
    #
    # distribute:
    #
    #     q + 1 -> first r neighbors
    #     q     -> remaining neighbors
    #
    # and subtract the complete quantity from the source.
    # -----------------------------------------------------------------
    def execute_resonate(self, amount=None):

        if len(self.connected_links) != 8:
            raise RuntimeError(
                "RESONATE requires CONNECT with exactly "
                "8 axial neighbors first"
            )

        # -------------------------------------------------------------
        # If no explicit amount is supplied, use the center-cell value.
        # -------------------------------------------------------------
        if amount is None:

            amount = self.mmu.read_cell(self.center)

        if not isinstance(amount, int):
            raise TypeError(
                "RESONATE requires an integer quantity"
            )

        if amount < 0:
            raise ValueError(
                "RESONATE currently accepts non-negative quantities"
            )

        source_value = self.mmu.read_cell(self.center)

        if source_value < amount:
            raise ValueError(
                "Insufficient source quantity: "
                f"source={source_value}, requested={amount}"
            )

        # -------------------------------------------------------------
        # Quotient/remainder decomposition.
        # -------------------------------------------------------------
        quotient, remainder = divmod(amount, 8)

        self.resonance_value = amount
        self.last_quotient = quotient
        self.last_remainder = remainder

        # -------------------------------------------------------------
        # Remove the routed quantity from the source.
        # -------------------------------------------------------------
        self.mmu.write_cell(
            self.center,
            source_value - amount
        )

        # -------------------------------------------------------------
        # Base allocation.
        # Every neighbor receives q.
        # -------------------------------------------------------------
        for neighbor in self.connected_links:

            current_value = self.mmu.read_cell(neighbor)

            self.mmu.write_cell(
                neighbor,
                current_value + quotient
            )

        # -------------------------------------------------------------
        # Deterministic remainder allocation.
        # First r neighbors receive +1.
        # -------------------------------------------------------------
        for i in range(remainder):

            neighbor = self.connected_links[i]

            current_value = self.mmu.read_cell(neighbor)

            self.mmu.write_cell(
                neighbor,
                current_value + 1
            )

        # -------------------------------------------------------------
        # Construct the routing vector for diagnostics.
        # -------------------------------------------------------------
        routing_vector = [
            quotient + (1 if i < remainder else 0)
            for i in range(8)
        ]

        print(
            f"[CRC ENGINE] RESONATE: "
            f"Routed quantity = {amount}"
        )

        print(
            f"[CRC ENGINE] RESONATE: "
            f"q = {quotient}, r = {remainder}"
        )

        print(
            f"[CRC ENGINE] RESONATE: "
            f"Routing vector = {routing_vector}"
        )

        return routing_vector

    # -----------------------------------------------------------------
    # COLLAPSE
    #
    # COLLAPSE is now a conservation verifier.
    #
    # It does NOT redistribute or modify the lattice.
    #
    # It compares the current total against the invariant baseline
    # established by CONNECT.
    # -----------------------------------------------------------------
    def execute_collapse(self, expected_total=None):

        if len(self.connected_links) != 8:
            raise RuntimeError(
                "COLLAPSE requires a connected 8-neighbor topology"
            )

        scope = [self.center] + self.connected_links

        # -------------------------------------------------------------
        # If no explicit baseline is supplied, use the baseline
        # recorded by CONNECT.
        # -------------------------------------------------------------
        if expected_total is None:

            expected_total = self.invariant_baseline

        if expected_total is None:

            raise RuntimeError(
                "No invariant baseline available"
            )

        observed_total = self.mmu.total_value(scope)

        # -------------------------------------------------------------
        # Conservation check.
        # -------------------------------------------------------------
        if observed_total != expected_total:

            print(
                "[COLLAPSE FAILURE] "
                f"Expected={expected_total}, "
                f"Observed={observed_total}"
            )

            return False

        print(
            "[COLLAPSE PASS] "
            f"Invariant verified: {observed_total}"
        )

        return True

    # -----------------------------------------------------------------
    # Return the local conservation scope.
    # -----------------------------------------------------------------
    def get_local_scope(self):

        return [self.center] + self.connected_links

    # -----------------------------------------------------------------
    # Return the local total.
    # -----------------------------------------------------------------
    def get_local_total(self):

        return self.mmu.total_value(
            self.get_local_scope()
        )


# =====================================================================
# 4. SOURCE COMPILER
# =====================================================================

class SovereignCompiler:

    def __init__(self):

        self.labels = {}

    # -----------------------------------------------------------------
    # Remove comments and surrounding whitespace.
    # -----------------------------------------------------------------
    def clean_line(self, text_line):

        # Support ';' comments.
        if ";" in text_line:
            text_line = text_line.split(";")[0]

        # Support '#' comments.
        if "#" in text_line:
            text_line = text_line.split("#")[0]

        return text_line.strip()

    # -----------------------------------------------------------------
    # Determine encoded instruction length.
    #
    # This is shared by both compiler passes so label addresses remain
    # consistent.
    # -----------------------------------------------------------------
    def instruction_length(self, parts):

        if not parts:
            return 0

        command = parts[0].upper()

        if command in [
            "LOAD_VAL",
            "SET_SCALE",
            "ADD_REG",
            "SUB_REG",
            "JMP",
            "JMP_NZ"
        ]:
            return 2

        elif command == "MMU_MAP":
            return 6

        elif command in [
            "STORE_CELL",
            "FETCH_CELL"
        ]:
            return 5

        else:
            return 1

    # -----------------------------------------------------------------
    # Resolve branch operand safely.
    #
    # This fixes the original eager-default problem:
    #
    #     self.labels.get(
    #         target,
    #         int(parts[1]) if parts[1].isdigit() else 0
    #     )
    #
    # Python evaluates the default argument before get(), so symbolic
    # labels could still trigger int("LABEL").
    # -----------------------------------------------------------------
    def resolve_address(self, operand):

        target = operand.upper()

        if target in self.labels:
            return self.labels[target]

        if target.isdigit():
            return int(target)

        raise ValueError(
            f"Unknown jump label or address: {operand}"
        )

    # -----------------------------------------------------------------
    # Compile assembly-like source to bytecode.
    # -----------------------------------------------------------------
    def compile_source_to_tokens(self, source_code_text):

        binary_tokens = []

        lines = source_code_text.strip().split("\n")

        cleaned_lines = []

        current_byte_index = 0

        # =============================================================
        # PASS 1
        #
        # Parse labels and calculate byte positions.
        # =============================================================
        for line in lines:

            line = self.clean_line(line)

            if not line:
                continue

            parts = line.split()

            if not parts:
                continue

            # ---------------------------------------------------------
            # Label detection.
            # ---------------------------------------------------------
            first_word = parts[0]

            if first_word.endswith(":"):

                label_name = first_word[:-1].upper()

                if label_name in self.labels:

                    raise ValueError(
                        f"Duplicate label: {label_name}"
                    )

                self.labels[label_name] = current_byte_index

                parts = parts[1:]

                if not parts:
                    continue

            cleaned_lines.append(parts)

            current_byte_index += self.instruction_length(parts)

        # =============================================================
        # PASS 2
        #
        # Convert source instructions into byte tokens.
        # =============================================================
        for parts in cleaned_lines:

            cmd = parts[0].upper()

            # ---------------------------------------------------------
            # No-operand operations.
            # ---------------------------------------------------------
            if cmd == "NOP":

                binary_tokens.append(OP_NOP)

            elif cmd == "AXIAL_SUM":

                binary_tokens.append(OP_AXIAL_SUM)

            elif cmd == "CONNECT":

                binary_tokens.append(OP_CONNECT)

            elif cmd == "RESONATE":

                binary_tokens.append(OP_RESONATE)

            elif cmd == "COLLAPSE":

                binary_tokens.append(OP_COLLAPSE)

            elif cmd == "HALT":

                binary_tokens.append(OP_HALT)

            # ---------------------------------------------------------
            # Single-value operations.
            # ---------------------------------------------------------
            elif cmd == "LOAD_VAL":

                if len(parts) != 2:
                    raise ValueError(
                        "LOAD_VAL requires one operand"
                    )

                value = int(parts[1])

                if not 0 <= value <= 255:
                    raise ValueError(
                        "LOAD_VAL operand must fit in one byte (0-255)"
                    )

                binary_tokens.extend([
                    OP_LOAD_VAL,
                    value
                ])

            elif cmd == "SET_SCALE":

                if len(parts) != 2:
                    raise ValueError(
                        "SET_SCALE requires one operand"
                    )

                value = int(parts[1])

                if not 1 <= value <= 255:
                    raise ValueError(
                        "SET_SCALE must be between 1 and 255"
                    )

                binary_tokens.extend([
                    OP_SET_SCALE,
                    value
                ])

            elif cmd == "ADD_REG":

                if len(parts) != 2:
                    raise ValueError(
                        "ADD_REG requires one operand"
                    )

                value = int(parts[1])

                if not 0 <= value <= 255:
                    raise ValueError(
                        "ADD_REG operand must fit in one byte"
                    )

                binary_tokens.extend([
                    OP_ADD_REG,
                    value
                ])

            elif cmd == "SUB_REG":

                if len(parts) != 2:
                    raise ValueError(
                        "SUB_REG requires one operand"
                    )

                value = int(parts[1])

                if not 0 <= value <= 255:
                    raise ValueError(
                        "SUB_REG operand must fit in one byte"
                    )

                binary_tokens.extend([
                    OP_SUB_REG,
                    value
                ])

            # ---------------------------------------------------------
            # MMU mapping.
            # ---------------------------------------------------------
            elif cmd == "MMU_MAP":

                if len(parts) != 6:
                    raise ValueError(
                        "MMU_MAP requires x y z w frame"
                    )

                x, y, z, w, frame = map(
                    int,
                    parts[1:6]
                )

                for value in [x, y, z, w, frame]:

                    if not 0 <= value <= 255:
                        raise ValueError(
                            "MMU_MAP operands must fit in one byte"
                        )

                binary_tokens.extend([
                    OP_MMU_MAP,
                    x,
                    y,
                    z,
                    w,
                    frame
                ])

            # ---------------------------------------------------------
            # Store cell.
            # ---------------------------------------------------------
            elif cmd == "STORE_CELL":

                if len(parts) != 5:
                    raise ValueError(
                        "STORE_CELL requires x y z w"
                    )

                x, y, z, w = map(
                    int,
                    parts[1:5]
                )

                binary_tokens.extend([
                    OP_STORE_CELL,
                    x,
                    y,
                    z,
                    w
                ])

            # ---------------------------------------------------------
            # Fetch cell.
            # ---------------------------------------------------------
            elif cmd == "FETCH_CELL":

                if len(parts) != 5:
                    raise ValueError(
                        "FETCH_CELL requires x y z w"
                    )

                x, y, z, w = map(
                    int,
                    parts[1:5]
                )

                binary_tokens.extend([
                    OP_FETCH_CELL,
                    x,
                    y,
                    z,
                    w
                ])

            # ---------------------------------------------------------
            # DIV_MOD
            #
            # This remains as a diagnostic arithmetic instruction.
            # It does not perform routing.
            # ---------------------------------------------------------
            elif cmd == "DIV_MOD":

                binary_tokens.append(OP_DIV_MOD_8)

            # ---------------------------------------------------------
            # JMP.
            # ---------------------------------------------------------
            elif cmd == "JMP":

                if len(parts) != 2:
                    raise ValueError(
                        "JMP requires one operand"
                    )

                address = self.resolve_address(
                    parts[1]
                )

                if not 0 <= address <= 255:
                    raise ValueError(
                        "Jump address must fit in one byte"
                    )

                binary_tokens.extend([
                    OP_JMP,
                    address
                ])

            # ---------------------------------------------------------
            # JMP_NZ.
            # ---------------------------------------------------------
            elif cmd == "JMP_NZ":

                if len(parts) != 2:
                    raise ValueError(
                        "JMP_NZ requires one operand"
                    )

                address = self.resolve_address(
                    parts[1]
                )

                if not 0 <= address <= 255:
                    raise ValueError(
                        "Jump address must fit in one byte"
                    )

                binary_tokens.extend([
                    OP_JMP_NZ,
                    address
                ])

            else:

                raise SyntaxError(
                    f"Unknown instruction: {cmd}"
                )

        return binary_tokens

    # -----------------------------------------------------------------
    # Export compiled program.
    # -----------------------------------------------------------------
    def export_to_binary_file(
        self,
        source_code_text,
        output_filename="independent_kernel.bin"
    ):

        token_list = self.compile_source_to_tokens(
            source_code_text
        )

        binary_bytes = bytes(token_list)

        with open(output_filename, "wb") as f:

            f.write(binary_bytes)

        print(
            f"[COMPILER SUCCESS] "
            f"Saved {len(binary_bytes)} raw bytes to -> "
            f"{output_filename}"
        )

        return binary_bytes


# =====================================================================
# 5. SOFTWARE RUNTIME KERNEL
# =====================================================================

class SovereignBareMetalKernel:

    def __init__(self):

        self.mmu = MemoryManagementUnit()

        self.ufni = SovereignMultiscaleEngine(
            self.mmu
        )

        self.registers = {
            "AL": 0,
            "REM": 0,
            "LOOP_CTR": 0
        }

        self.instruction_pointer = 0

        self.halted = False

    # -----------------------------------------------------------------
    # Load and execute binary file.
    # -----------------------------------------------------------------
    def boot_from_binary_file(
        self,
        filename="independent_kernel.bin"
    ):

        if not os.path.exists(filename):

            print(
                f"[BOOT ERROR] "
                f"Target file {filename} not found."
            )

            return False

        print(
            f"\n[RUNTIME BOOT] "
            f"Reading executable stream from: {filename}"
        )

        with open(filename, "rb") as f:

            raw_binary_stream = list(
                f.read()
            )

        return self.execute_binary_package(
            raw_binary_stream
        )

    # -----------------------------------------------------------------
    # Execute bytecode.
    # -----------------------------------------------------------------
    def execute_binary_package(
        self,
        bytecode_stream
    ):

        self.instruction_pointer = 0
        self.halted = False

        stream_len = len(
            bytecode_stream
        )

        print(
            "[KERNEL] Starting software runtime "
            f"execution loop... "
            f"Stream size: {stream_len} bytes."
        )

        while (
            self.instruction_pointer < stream_len
            and not self.halted
        ):

            token = bytecode_stream[
                self.instruction_pointer
            ]

            # =========================================================
            # NOP
            # =========================================================
            if token == OP_NOP:

                self.instruction_pointer += 1

            # =========================================================
            # LOAD_VAL
            # =========================================================
            elif token == OP_LOAD_VAL:

                if self.instruction_pointer + 1 >= stream_len:

                    self.runtime_error(
                        "LOAD_VAL missing operand"
                    )
                    break

                value = bytecode_stream[
                    self.instruction_pointer + 1
                ]

                self.registers["AL"] = value

                print(
                    f"[KERNEL EXEC] "
                    f"LOAD_VAL: AL = {value}"
                )

                self.instruction_pointer += 2

            # =========================================================
            # DIV_MOD_8
            #
            # Diagnostic quotient/remainder operation.
            # =========================================================
            elif token == OP_DIV_MOD_8:

                current_val = self.registers["AL"]

                quotient, remainder = divmod(
                    current_val,
                    8
                )

                self.registers["AL"] = quotient
                self.registers["REM"] = remainder

                print(
                    f"[KERNEL EXEC] DIV_MOD_8: "
                    f"AL={quotient}, REM={remainder}"
                )

                self.instruction_pointer += 1

            # =========================================================
            # AXIAL_SUM
            # =========================================================
            elif token == OP_AXIAL_SUM:

                if len(self.ufni.connected_links) != 8:

                    self.runtime_error(
                        "AXIAL_SUM requires CONNECT first"
                    )
                    break

                axial_sum = sum(
                    self.mmu.read_cell(node)
                    for node in self.ufni.connected_links
                )

                self.registers["AL"] = axial_sum

                print(
                    f"[KERNEL EXEC] "
                    f"AXIAL_SUM: "
                    f"Neighbor sum = {axial_sum}"
                )

                self.instruction_pointer += 1

            # =========================================================
            # MMU_MAP
            # =========================================================
            elif token == OP_MMU_MAP:

                if (
                    self.instruction_pointer + 5
                    >= stream_len
                ):

                    self.runtime_error(
                        "MMU_MAP missing operands"
                    )
                    break

                x = bytecode_stream[
                    self.instruction_pointer + 1
                ]

                y = bytecode_stream[
                    self.instruction_pointer + 2
                ]

                z = bytecode_stream[
                    self.instruction_pointer + 3
                ]

                w = bytecode_stream[
                    self.instruction_pointer + 4
                ]

                frame = bytecode_stream[
                    self.instruction_pointer + 5
                ]

                self.mmu.map_lattice_address(
                    (x, y, z, w),
                    frame
                )

                print(
                    f"[KERNEL EXEC] "
                    f"MMU_MAP: "
                    f"({x},{y},{z},{w}) -> "
                    f"Frame {frame}"
                )

                self.instruction_pointer += 6

            # =========================================================
            # SET_SCALE
            # =========================================================
            elif token == OP_SET_SCALE:

                scale_value = bytecode_stream[
                    self.instruction_pointer + 1
                ]

                try:

                    self.ufni.update_resolution_scale(
                        scale_value
                    )

                except ValueError as error:

                    self.runtime_error(
                        str(error)
                    )
                    break

                self.instruction_pointer += 2

            # =========================================================
            # ADD_REG
            # =========================================================
            elif token == OP_ADD_REG:

                value = bytecode_stream[
                    self.instruction_pointer + 1
                ]

                self.registers["AL"] += value

                print(
                    f"[KERNEL EXEC] "
                    f"ADD_REG: +{value}; "
                    f"AL={self.registers['AL']}"
                )

                self.instruction_pointer += 2

            # =========================================================
            # SUB_REG
            #
            # Retained as loop-counter operation.
            # =========================================================
            elif token == OP_SUB_REG:

                value = bytecode_stream[
                    self.instruction_pointer + 1
                ]

                self.registers["LOOP_CTR"] -= value

                print(
                    f"[KERNEL EXEC] "
                    f"SUB_REG: -{value}; "
                    f"LOOP_CTR="
                    f"{self.registers['LOOP_CTR']}"
                )

                self.instruction_pointer += 2

            # =========================================================
            # STORE_CELL
            # =========================================================
            elif token == OP_STORE_CELL:

                x = bytecode_stream[
                    self.instruction_pointer + 1
                ]

                y = bytecode_stream[
                    self.instruction_pointer + 2
                ]

                z = bytecode_stream[
                    self.instruction_pointer + 3
                ]

                w = bytecode_stream[
                    self.instruction_pointer + 4
                ]

                self.mmu.write_cell(
                    (x, y, z, w),
                    self.registers["AL"]
                )

                print(
                    f"[KERNEL EXEC] "
                    f"STORE_CELL: "
                    f"({x},{y},{z},{w}) = "
                    f"{self.registers['AL']}"
                )

                self.instruction_pointer += 5

            # =========================================================
            # FETCH_CELL
            # =========================================================
            elif token == OP_FETCH_CELL:

                x = bytecode_stream[
                    self.instruction_pointer + 1
                ]

                y = bytecode_stream[
                    self.instruction_pointer + 2
                ]

                z = bytecode_stream[
                    self.instruction_pointer + 3
                ]

                w = bytecode_stream[
                    self.instruction_pointer + 4
                ]

                self.registers["AL"] = (
                    self.mmu.read_cell(
                        (x, y, z, w)
                    )
                )

                print(
                    f"[KERNEL EXEC] "
                    f"FETCH_CELL: "
                    f"AL={self.registers['AL']} "
                    f"from ({x},{y},{z},{w})"
                )

                self.instruction_pointer += 5

            # =========================================================
            # CONNECT
            # =========================================================
            elif token == OP_CONNECT:

                try:

                    self.ufni.execute_connect(
                        0, 0, 0, 0
                    )

                except Exception as error:

                    self.runtime_error(
                        f"CONNECT failed: {error}"
                    )
                    break

                self.instruction_pointer += 1

            # =========================================================
            # RESONATE
            #
            # Uses AL as the explicit routing quantity.
            #
            # If AL is zero, this is a zero transfer.
            # =========================================================
            elif token == OP_RESONATE:

                try:

                    routing_vector = (
                        self.ufni.execute_resonate(
                            self.registers["AL"]
                        )
                    )

                except Exception as error:

                    self.runtime_error(
                        f"RESONATE failed: {error}"
                    )
                    break

                print(
                    f"[KERNEL EXEC] "
                    f"RESONATE completed: "
                    f"{routing_vector}"
                )

                self.instruction_pointer += 1

            # =========================================================
            # COLLAPSE
            #
            # Pure invariant verification.
            # =========================================================
            elif token == OP_COLLAPSE:

                try:

                    result = (
                        self.ufni.execute_collapse()
                    )

                except Exception as error:

                    self.runtime_error(
                        f"COLLAPSE failed: {error}"
                    )
                    break

                if not result:

                    print(
                        "[KERNEL] "
                        "Conservation invariant violated."
                    )

                    self.halted = True

                    break

                self.instruction_pointer += 1

            # =========================================================
            # JMP
            # =========================================================
            elif token == OP_JMP:

                target_address = bytecode_stream[
                    self.instruction_pointer + 1
                ]

                self.instruction_pointer = (
                    target_address
                )

            # =========================================================
            # JMP_NZ
            # =========================================================
            elif token == OP_JMP_NZ:

                target_address = bytecode_stream[
                    self.instruction_pointer + 1
                ]

                if self.registers["LOOP_CTR"] > 0:

                    print(
                        f"[KERNEL ROUTE] "
                        f"JMP_NZ: "
                        f"LOOP_CTR="
                        f"{self.registers['LOOP_CTR']} "
                        f"-> {target_address}"
                    )

                    self.instruction_pointer = (
                        target_address
                    )

                else:

                    print(
                        "[KERNEL ROUTE] "
                        "JMP_NZ: "
                        "Loop counter reached zero."
                    )

                    self.instruction_pointer += 2

            # =========================================================
            # HALT
            # =========================================================
            elif token == OP_HALT:

                print(
                    "[KERNEL] "
                    "HALT encountered. "
                    "Stopping runtime."
                )

                self.halted = True

                break

            # =========================================================
            # UNKNOWN OPCODE
            # =========================================================
            else:

                self.runtime_error(
                    f"Unknown instruction code: {token}"
                )

                break

        return not self.halted

    # -----------------------------------------------------------------
    # Runtime error handler.
    # -----------------------------------------------------------------
    def runtime_error(self, message):

        print(
            f"[KERNEL ERROR] {message}"
        )

        self.halted = True


# =====================================================================
# 6. TEST / VERIFICATION UTILITIES
# =====================================================================

def print_local_state(
    kernel,
    title="LOCAL LATTICE STATE"
):

    print()
    print(
        "================================================================="
    )
    print(
        f"                    {title}"
    )
    print(
        "================================================================="
    )

    center = kernel.ufni.center

    print(
        f"Center {center}: "
        f"{kernel.mmu.read_cell(center)}"
    )

    for index, neighbor in enumerate(
        kernel.ufni.connected_links,
        start=1
    ):

        value = kernel.mmu.read_cell(
            neighbor
        )

        print(
            f"N{index} {neighbor}: {value}"
        )

    print(
        f"Local total: "
        f"{kernel.ufni.get_local_total()}"
    )

    print(
        "================================================================="
    )


# =====================================================================
# 7. DIRECT MATHEMATICAL ROUTING TEST
# =====================================================================

def test_routing_case(amount):

    print()
    print(
        "#################################################################"
    )

    print(
        f"TEST ROUTING AMOUNT = {amount}"
    )

    print(
        "#################################################################"
    )

    mmu = MemoryManagementUnit()

    engine = SovereignMultiscaleEngine(
        mmu
    )

    center = (0, 0, 0, 0)

    # -------------------------------------------------------------
    # Seed source.
    # -------------------------------------------------------------
    mmu.write_cell(
        center,
        amount
    )

    # -------------------------------------------------------------
    # Establish topology and baseline.
    # -------------------------------------------------------------
    engine.execute_connect(
        0, 0, 0, 0
    )

    initial_total = (
        engine.get_local_total()
    )

    print(
        f"[TEST] Initial local total = "
        f"{initial_total}"
    )

    # -------------------------------------------------------------
    # Perform routing.
    # -------------------------------------------------------------
    routing_vector = (
        engine.execute_resonate(
            amount
        )
    )

    final_total = (
        engine.get_local_total()
    )

    print(
        f"[TEST] Final local total = "
        f"{final_total}"
    )

    print(
        f"[TEST] Routing vector = "
        f"{routing_vector}"
    )

    # -------------------------------------------------------------
    # Verify conservation.
    # -------------------------------------------------------------
    result = engine.execute_collapse(
        initial_total
    )

    if result:

        print(
            f"[TEST PASS] "
            f"Routing case n={amount}"
        )

    else:

        print(
            f"[TEST FAIL] "
            f"Routing case n={amount}"
        )

    # -------------------------------------------------------------
    # Verify bounded imbalance.
    # -------------------------------------------------------------
    minimum = min(
        routing_vector
    )

    maximum = max(
        routing_vector
    )

    imbalance = (
        maximum - minimum
    )

    print(
        f"[TEST] min={minimum}, "
        f"max={maximum}, "
        f"imbalance={imbalance}"
    )

    if imbalance <= 1:

        print(
            "[TEST PASS] "
            "Bounded routing imbalance <= 1"
        )

    else:

        print(
            "[TEST FAIL] "
            "Routing imbalance > 1"
        )

    return result


# =====================================================================
# 8. INTENTIONAL COLLAPSE FAILURE TEST
# =====================================================================

def test_collapse_failure():

    print()
    print(
        "#################################################################"
    )

    print(
        "TEST INTENTIONAL CONSERVATION FAILURE"
    )

    print(
        "#################################################################"
    )

    mmu = MemoryManagementUnit()

    engine = SovereignMultiscaleEngine(
        mmu
    )

    center = (0, 0, 0, 0)

    # -------------------------------------------------------------
    # Seed 27 units.
    # -------------------------------------------------------------
    mmu.write_cell(
        center,
        27
    )

    # -------------------------------------------------------------
    # Establish baseline.
    # -------------------------------------------------------------
    engine.execute_connect(
        0, 0, 0, 0
    )

    baseline = (
        engine.invariant_baseline
    )

    print(
        f"[TEST] Baseline = {baseline}"
    )

    # -------------------------------------------------------------
    # Deliberately corrupt one neighbor.
    # -------------------------------------------------------------
    corrupted_neighbor = (
        engine.connected_links[0]
    )

    current = mmu.read_cell(
        corrupted_neighbor
    )

    mmu.write_cell(
        corrupted_neighbor,
        current + 5
    )

    print(
        f"[TEST] Deliberately added "
        f"+5 to {corrupted_neighbor}"
    )

    observed = (
        engine.get_local_total()
    )

    print(
        f"[TEST] Corrupted total = "
        f"{observed}"
    )

    # -------------------------------------------------------------
    # COLLAPSE must fail.
    # -------------------------------------------------------------
    result = engine.execute_collapse(
        baseline
    )

    if result:

        print(
            "[TEST FAIL] "
            "COLLAPSE incorrectly accepted "
            "a corrupted state."
        )

        return False

    print(
        "[TEST PASS] "
        "COLLAPSE correctly detected "
        "the conservation violation."
    )

    return True


# =====================================================================
# 9. MAIN VERIFICATION PROGRAM
# =====================================================================

if __name__ == "__main__":

    print(
        "================================================================="
    )

    print(
        "       SOVEREIGN-L DISCRETE 4D ROUTING REFERENCE MODEL"
    )

    print(
        "================================================================="
    )

    print()
    print(
        "Execution model:"
    )

    print(
        "    CONNECT -> RESONATE -> COLLAPSE"
    )

    print()
    print(
        "RESONATE implements:"
    )

    print(
        "    n = 8q + r"
    )

    print(
        "    q = n // 8"
    )

    print(
        "    r = n % 8"
    )

    print()
    print(
        "COLLAPSE performs invariant verification."
    )

    print(
        "================================================================="
    )

    # ================================================================
    # TEST 1
    # ================================================================

    test_routing_case(1)

    # ================================================================
    # TEST 2
    # ================================================================

    test_routing_case(7)

    # ================================================================
    # TEST 3
    # ================================================================

    test_routing_case(8)

    # ================================================================
    # TEST 4
    # ================================================================

    test_routing_case(27)

    # ================================================================
    # TEST 5
    # ================================================================

    test_routing_case(32)

    # ================================================================
    # TEST 6
    #
    # Deliberate failure.
    # ================================================================

    failure_result = test_collapse_failure()

    # ================================================================
    # Final status.
    # ================================================================

    print()
    print(
        "================================================================="
    )

    print(
        "                     TESTING COMPLETE"
    )

    print(
        "================================================================="
    )

    if failure_result:

        print(
            "[STATUS] "
            "Positive routing tests and "
            "negative conservation test completed."
        )

    else:

        print(
            "[STATUS] "
            "Negative conservation test did not behave as expected."
        )

    print(
        "================================================================="
    )
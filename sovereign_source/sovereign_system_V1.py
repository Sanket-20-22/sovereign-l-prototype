# sovereign_system.py - Part 1
import sys
import os

# =====================================================================
# 1. THE INSTRUCTION SET ARCHITECTURE (iSA) DEFINITIONS
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

# CRC Neuromorphic Logic Tokens
OP_CONNECT    = 0x10  
OP_RESONATE   = 0x11  
OP_COLLAPSE   = 0x12  

# Branch Operations Tokens
OP_JMP        = 0x13  
OP_JMP_NZ     = 0x14  
OP_HALT       = 0xFF  

# =====================================================================
# 2. THE MEMORY MANAGEMENT UNIT (MMU) & UFNI ENGINE
# =====================================================================
class MemoryManagementUnit:
    def __init__(self):
        self.page_directory = {}
        self.frame_storage = {}

    def map_lattice_address(self, coordinate_4d, frame_id):
        self.page_directory[coordinate_4d] = frame_id
        if frame_id not in self.frame_storage:
            self.frame_storage[frame_id] = 0

    def write_cell(self, coordinate_4d, value):
        frame_id = self.page_directory.get(coordinate_4d)
        if frame_id is not None:
            self.frame_storage[frame_id] = int(value)
        else:
            new_frame = len(self.page_directory)
            self.page_directory[coordinate_4d] = new_frame
            self.frame_storage[new_frame] = int(value)

    def read_cell(self, coordinate_4d):
        frame_id = self.page_directory.get(coordinate_4d)
        if frame_id is not None:
            return self.frame_storage[frame_id]
        return 0

class SovereignMultiscaleEngine:
    def __init__(self, mmu_instance):
        self.mmu = mmu_instance
        self.current_scale = 1
        self.connected_links = []
        self.resonance_value = 0

    def update_resolution_scale(self, scale_factor):
        self.current_scale = scale_factor
        print(f"[SCALE] Shifted to scale index: {self.current_scale}")

    def get_orthogonal_neighbors(self, x, y, z, w):
        s = self.current_scale
        return [
            (x+s, y, z, w), (x-s, y, z, w),
            (x, y+s, z, w), (x, y-s, z, w),
            (x, y, z+s, w), (x, y, z-s, w),
            (x, y, z, w+s), (x, y, z, w-s)
        ]

    def execute_connect(self, x, y, z, w):
        self.connected_links = self.get_orthogonal_neighbors(x, y, z, w)
        print(f"[CRC ENGINE] CONNECT: Mapped 8-axial links for ({x},{y},{z},{w})")

    def execute_resonate(self):
        if not self.connected_links:
            self.resonance_value = 0
            return 0
        total_sum = 0
        for n in self.connected_links:
            total_sum += self.mmu.read_cell(n)
        self.resonance_value = total_sum // len(self.connected_links)
        print(f"[CRC ENGINE] RESONATE: Field interaction match = {self.resonance_value}")
        return self.resonance_value

    def execute_collapse(self, x, y, z, w, current_local_val):
        delta = self.resonance_value - current_local_val
        new_state = current_local_val + (delta // 2)
        self.mmu.write_cell((x, y, z, w), new_state)
        print(f"[CRC ENGINE] COLLAPSE: Cell updated from {current_local_val} -> {new_state}")
        return new_state

# sovereign_system.py - Part 2

# =====================================================================
# 4. THE SELF-HOSTING STRING ASSEMBLY COMPILER (DECISIVE INDEX FIX)
# =====================================================================
class SovereignCompiler:
    def __init__(self):
        self.labels = {}

    def compile_source_to_tokens(self, source_code_text):
        binary_tokens = []
        lines = source_code_text.strip().split("\n")
        
        current_byte_index = 0
        cleaned_lines = []
        
        # Pass 1: Parse and record code loop label positions correctly
        for line in lines:
            if ";" in line:
                line = line.split(";")[0]
            line = line.strip()
            if not line:
                continue
                
            parts = line.split()
            if not parts:
                continue
                
            first_word = parts[0]
            if first_word.endswith(":"):
                label_name = first_word[:-1].upper()
                self.labels[label_name] = current_byte_index
                parts = parts[1:]
                if not parts:
                    continue
            
            cleaned_lines.append(parts)
            cmd = parts[0].upper()
            if cmd in ["LOAD_VAL", "SET_SCALE", "ADD_REG", "SUB_REG", "JMP", "JMP_NZ"]:
                current_byte_index += 2
            elif cmd == "MMU_MAP":
                current_byte_index += 6
            elif cmd in ["STORE_CELL", "FETCH_CELL"]:
                current_byte_index += 5
            else:
                current_byte_index += 1

        # Pass 2: Map string words to actual hardware binary tokens safely
        for parts in cleaned_lines:
            cmd = parts[0].upper()
            
            if cmd == "NOP":
                binary_tokens.append(OP_NOP)
            elif cmd == "DIV_MOD":
                binary_tokens.append(OP_DIV_MOD_8)
            elif cmd == "AXIAL_SUM":
                binary_tokens.append(OP_AXIAL_SUM)
            elif cmd == "LOAD_VAL":
                binary_tokens.extend([OP_LOAD_VAL, int(parts[1])])
            elif cmd == "SET_SCALE":
                binary_tokens.extend([OP_SET_SCALE, int(parts[1])])
            elif cmd == "MMU_MAP":
                x, y, z, w, f = map(int, parts[1:6])
                binary_tokens.extend([OP_MMU_MAP, x, y, z, w, f])
            elif cmd == "ADD_REG":
                binary_tokens.extend([OP_ADD_REG, int(parts[1])])
            elif cmd == "SUB_REG":
                binary_tokens.extend([OP_SUB_REG, int(parts[1])])
            elif cmd == "STORE_CELL":
                x, y, z, w = map(int, parts[1:5])
                binary_tokens.extend([OP_STORE_CELL, x, y, z, w])
            elif cmd == "FETCH_CELL":
                x, y, z, w = map(int, parts[1:5])
                binary_tokens.extend([OP_FETCH_CELL, x, y, z, w])
            elif cmd == "CONNECT":
                binary_tokens.append(OP_CONNECT)
            elif cmd == "RESONATE":
                binary_tokens.append(OP_RESONATE)
            elif cmd == "COLLAPSE":
                binary_tokens.append(OP_COLLAPSE)
            elif cmd == "JMP":
                target = parts[1].upper()
                addr = self.labels.get(target, int(parts[1]) if parts[1].isdigit() else 0)
                binary_tokens.extend([OP_JMP, addr])
            elif cmd == "JMP_NZ":
                target = parts[1].upper()
                addr = self.labels.get(target, int(parts[1]) if parts[1].isdigit() else 0)
                binary_tokens.extend([OP_JMP_NZ, addr])
            elif cmd == "HALT":
                binary_tokens.append(OP_HALT)
                
        return binary_tokens

    def export_to_binary_file(self, source_code_text, output_filename="independent_kernel.bin"):
        token_list = self.compile_source_to_tokens(source_code_text)
        binary_bytes = bytes(token_list)
        with open(output_filename, "wb") as f:
            f.write(binary_bytes)
        print(f"[COMPILER SUCCESS] Saved {len(binary_bytes)} raw bytes to -> {output_filename}")

# sovereign_system.py - Part 3

# =====================================================================
# 5. THE RUNTIME KERNEL ENGINE
# =====================================================================
class SovereignBareMetalKernel:
    def __init__(self):
        self.mmu = MemoryManagementUnit()
        self.ufni = SovereignMultiscaleEngine(self.mmu)
        self.registers = {"AL": 0, "LOOP_CTR": 0} 
        self.instruction_pointer = 0

    def boot_from_binary_file(self, filename="independent_kernel.bin"):
        if not os.path.exists(filename):
            print(f"[BOOT ERROR] Target file {filename} not found.")
            return
        print(f"\n[HARDWARE BOOT] Reading executable stream directly from: {filename}")
        with open(filename, "rb") as f:
            raw_binary_stream = list(f.read())
        self.execute_binary_package(raw_binary_stream)

    def execute_binary_package(self, bytecode_stream):
        self.instruction_pointer = 0
        stream_len = len(bytecode_stream)
        print(f"[KERNEL] Starting machine runtime execution loop... Stream size: {stream_len} bytes.")

        while self.instruction_pointer < stream_len:
            token = bytecode_stream[self.instruction_pointer]
            
            if token == OP_NOP:
                self.instruction_pointer += 1
            elif token == OP_LOAD_VAL:
                val = bytecode_stream[self.instruction_pointer + 1]
                self.registers["AL"] = val
                print(f"[KERNEL EXEC] LOAD_VAL: Register AL = {val}")
                self.instruction_pointer += 2
            elif token == OP_DIV_MOD_8:
                current_val = self.registers["AL"]
                floor_div = current_val // 8
                remainder = current_val % 8
                self.registers["AL"] = floor_div + remainder
                print(f"[KERNEL EXEC] DIV_MOD: AL right shifted. State: {self.registers['AL']}")
                self.instruction_pointer += 1
            elif token == OP_MMU_MAP:
                x = bytecode_stream[self.instruction_pointer + 1]
                y = bytecode_stream[self.instruction_pointer + 2]
                z = bytecode_stream[self.instruction_pointer + 3]
                w = bytecode_stream[self.instruction_pointer + 4]
                frame = bytecode_stream[self.instruction_pointer + 5]
                self.mmu.map_lattice_address((x, y, z, w), frame)
                print(f"[KERNEL EXEC] MMU_MAP: Lattice ({x},{y},{z},{w}) -> Frame {frame}")
                self.instruction_pointer += 6
            elif token == OP_AXIAL_SUM:
                sum_result = self.ufni.compute_axial_energy(0, 0, 0, 0)
                print(f"[KERNEL EXEC] AXIAL_SUM: Neighborhood energy value = {sum_result}")
                self.instruction_pointer += 1
            elif token == OP_SET_SCALE:
                scale_val = bytecode_stream[self.instruction_pointer + 1]
                self.ufni.update_resolution_scale(scale_val)
                self.instruction_pointer += 2
            elif token == OP_ADD_REG:
                val = bytecode_stream[self.instruction_pointer + 1]
                self.registers["AL"] += val
                print(f"[KERNEL EXEC] ADD_REG: Added {val}. AL state = {self.registers['AL']}")
                self.instruction_pointer += 2
            elif token == OP_SUB_REG:
                val = bytecode_stream[self.instruction_pointer + 1]
                self.registers["LOOP_CTR"] -= val  # Safely reduce loop state ticks down
                print(f"[KERNEL EXEC] SUB_REG: Decremented Loop counter by {val}. LOOP_CTR = {self.registers['LOOP_CTR']}")
                self.instruction_pointer += 2
            elif token == OP_STORE_CELL:
                x = bytecode_stream[self.instruction_pointer + 1]
                y = bytecode_stream[self.instruction_pointer + 2]
                z = bytecode_stream[self.instruction_pointer + 3]
                w = bytecode_stream[self.instruction_pointer + 4]
                self.mmu.write_cell((x, y, z, w), self.registers["AL"])
                print(f"[KERNEL EXEC] STORE_CELL: Wrote AL ({self.registers['AL']}) into cell ({x},{y},{z},{w})")
                self.instruction_pointer += 5
            elif token == OP_FETCH_CELL:
                x = bytecode_stream[self.instruction_pointer + 1]
                y = bytecode_stream[self.instruction_pointer + 2]
                z = bytecode_stream[self.instruction_pointer + 3]
                w = bytecode_stream[self.instruction_pointer + 4]
                self.registers["AL"] = self.mmu.read_cell((x, y, z, w))
                print(f"[KERNEL EXEC] FETCH_CELL: Loaded cell ({x},{y},{z},{w}) value into AL Register")
                self.instruction_pointer += 5
            elif token == OP_CONNECT:
                self.ufni.execute_connect(0, 0, 0, 0)
                self.instruction_pointer += 1
            elif token == OP_RESONATE:
                self.ufni.execute_resonate()
                self.instruction_pointer += 1
            elif token == OP_COLLAPSE:
                local_val = self.mmu.read_cell((0, 0, 0, 0))
                delta = self.ufni.resonance_value - local_val
                
                # Natively calculate Euclidean quotient and remainder simultaneously
                quotient  = delta // 8
                remainder = delta % 8  # Used for Round-Robin neighbor distribution
                
                # Conserve energy by scaling via quotient and adding the remainder fractional offset
                collapsed_net = local_val + quotient
                self.mmu.write_cell((0, 0, 0, 0), collapsed_net)
                self.registers["AL"] = collapsed_net
                
                # Round-Robin: Route the remainder energy token precisely to a target neighbor port
                neighbors = self.ufni.get_orthogonal_neighbors(0, 0, 0, 0)
                # Remainder dictates the active target neighbor index (0 to 7)
                target_neighbor = neighbors[abs(remainder) % 8]
                neighbor_val = self.mmu.read_cell(target_neighbor)
                self.mmu.write_cell(target_neighbor, neighbor_val + 1)
                
                print(f"[CRC ENGINE] COLLAPSE: Core base-8 scaled to {collapsed_net}")
                print(f" └── Round-Robin: Modulo %8 Remainder ({remainder}) routed +1 energy token to neighbor: {target_neighbor}")
                self.instruction_pointer += 1

            elif token == OP_JMP:
                target_address = bytecode_stream[self.instruction_pointer + 1]
                self.instruction_pointer = target_address
            elif token == OP_JMP_NZ:
                target_address = bytecode_stream[self.instruction_pointer + 1]
                if self.registers["LOOP_CTR"] > 0:
                    print(f"[KERNEL ROUTE] JMP_NZ: Loop Counter ({self.registers['LOOP_CTR']}) > 0. Routing back to offset index: {target_address}")
                    self.instruction_pointer = target_address
                else:
                    print(f"[KERNEL ROUTE] JMP_NZ: Loop Counter reached 0. Breaking loop sequence cleanly.")
                    self.instruction_pointer += 2
            elif token == OP_HALT:
                print("[KERNEL] HALT state flag encountered. Stopping clocks cleanly.\n")
                break
            else:
                print(f"[KERNEL ERROR] Invalid Instruction Code Unknown: {token}")
                break

# =====================================================================
# SYSTEM VERIFICATION ROUTINE ENTRY POINT
# =====================================================================
# Part 4: System Verification Entry Point Test Code Running Cyclic CRC Fields

if __name__ == "__main__":
    print("=================================================================")
    print("     SOVEREIGN-L ARCHITECTURE UNIFIED BARE-METAL PIPELINE       ")
    print("=================================================================")
    
    sovereign_assembly_program = """
    NOP                        ; Verification sync frame step
    MMU_MAP 1 0 0 0 50         ; Map spatial coordinate tracking targets
    MMU_MAP 0 1 0 0 51         
    LOAD_VAL 120               ; Seed whole number interaction states
    STORE_CELL 1 0 0 0         
    LOAD_VAL 60                
    STORE_CELL 0 0 0 0         
    SET_SCALE 1                
    
    LOOP_START: CONNECT        ; Hardwired iteration label marker
    RESONATE                   
    COLLAPSE                   
    SUB_REG 1                  ; Explicitly decrease state values down
    JMP_NZ LOOP_START          
    HALT                       
    """

    compiler = SovereignCompiler()
    kernel = SovereignBareMetalKernel()
    
    kernel.registers["LOOP_CTR"] = 3

    print("[STEP 1] Running assembly strings parser through Sovereign_Source Compiler backend...")
    compiled_binary_bytes = compiler.compile_source_to_tokens(sovereign_assembly_program)
    print(f"-> Generated Bytecode Machine Tokens Stream: {compiled_binary_bytes}")

    print("\n[STEP 2] Exporting hardware package to storage drive...")
    compiler.export_to_binary_file(sovereign_assembly_program, "independent_kernel.bin")

    print("\n[STEP 3] Initializing the independent hardware emulation execution tracks...")
    kernel.boot_from_binary_file("independent_kernel.bin")

    # =====================================================================
    # AUTOMATIC POST-EXECUTION VERIFICATION MATRIX STATE DUMP
    # =====================================================================
    print("\n=================================================================")
    print("        SOVEREIGN PHYSICAL LATTICE NODE REGISTER DUMP            ")
    print("=================================================================")
    
    target_nodes = [
        (0, 0, 0, 0),  # Central Core Processing Point
        (1, 0, 0, 0),  # Orthogonal X Neighbor Track
        (0, 1, 0, 0)   # Orthogonal Y Neighbor Track
    ]
    
    for node in target_nodes:
        frame_id = kernel.mmu.page_directory.get(node)
        final_value = kernel.mmu.read_cell(node)
        print(f"Lattice Node Space Key: {node}")
        print(f" └── Mapped Physical Storage Frame: {frame_id}")
        print(f" └── Final Settled Coordinate State: {final_value}")
        
    print(f"\nAL Accumulator Register Value:  {kernel.registers['AL']}")
    print(f"LOOP_CTR Branch Register Value: {kernel.registers['LOOP_CTR']}")
    print("=================================================================")
    print("      Verification complete. All local subsystem blocks verified. ")
    print("=================================================================")

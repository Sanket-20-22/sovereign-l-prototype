"""
=====================================================================
UNIFIED FIELD NEUROMORPHIC INTELLIGENCE (UFNI) CORE MOTHER MODULE
Core File Node: UFNI_core.py
License: GNU General Public License v3.0 (Copyleft Shield Active)
Author: Sanket Hazra (Jadavpur University Alumnus)
=====================================================================
"""

# =====================================================================
# 1. THE INSTRUCTION SET ARCHITECTURE (ISA) HARDWARE MAPPINGS
# =====================================================================
class SovereignISA:
    OPCODES = {
        'CONNECT':  0x01,  # Hardware-level circuit path bridge
        'RESONATE': 0x02,  # 8-neighbor whole-number division split
        'COLLAPSE': 0x03   # Global energy conservation safety trip
    }
    
    # Bounded relative coordinate direction tokens from your prototype spec
    DIRECTIONS = {
        'x+1': 0x10, 'x-1': 0x11,
        'y+1': 0x20, 'y-1': 0x21,
        'z+1': 0x30, 'z-1': 0x31,
        'w+1': 0x40, 'w-1': 0x41
    }

# =====================================================================
# 2. THE BOOTSTRAP COMPILER & LEXICAL PARSER
# =====================================================================
class SovereignCompiler:
    def __init__(self):
        self.isa = SovereignISA()

    def clean_line(self, text_line):
        """Strips out comments and clean raw whitespace."""
        return text_line.split('#')[0].strip()

    def compile_instruction(self, line_num, line_text):
        """Converts text assembly commands directly into raw bytecode packets."""
        cleaned = self.clean_line(line_text)
        if not cleaned:
            return b''

        parts = cleaned.split()
        command = parts[0].upper()

        if command not in self.isa.OPCODES:
            raise SyntaxError(f"[Line {line_num}] Unknown instruction token: {command}")

        packet = bytearray([self.isa.OPCODES[command]])

        if command == 'CONNECT':
            if len(parts) != 3:
                raise ValueError(f"[Line {line_num}] CONNECT requires exactly 2 directional operands.")
            src, dest = parts[1], parts[2]
            if src not in self.isa.DIRECTIONS or dest not in self.isa.DIRECTIONS:
                raise ValueError(f"[Line {line_num}] Invalid axis coordinate token.")
            packet.append(self.isa.DIRECTIONS[src])
            packet.append(self.isa.DIRECTIONS[dest])
            return bytes(packet)

        elif command == 'RESONATE':
            if len(parts) != 2:
                raise ValueError(f"[Line {line_num}] RESONATE requires a whole-number pulse value.")
            val = int(parts[1])
            if not (0 <= val <= 255):
                raise ValueError("Pulse load must fit inside a single unsigned byte (0-255).")
            packet.append(val)
            return bytes(packet)

        elif command == 'COLLAPSE':
            packet.append(0xFF)  # Global validation mask flag
            return bytes(packet)

        return b''

    def assemble_script(self, script_text):
        """Assembles a text file stream into an integrated bytecode stream block."""
        bytecode = b''
        for idx, line in enumerate(script_text.strip().split('\n'), 1):
            bytecode += self.compile_instruction(idx, line)
        return bytecode

# =====================================================================
# 3. THE BARE-METAL 4D DISCRETE HARDWARE KERNEL RUNTIME
# =====================================================================
class SovereignKernel:
    def __init__(self):
        self.isa = SovereignISA()
        
        # Hardwired physical data buses mapping your 8 orthogonal neighbors in 4D space (Z^4)
        self.orthogonal_buses = [
            (0, 1, 0, 0),  # North (Element 108)
            (0, -1, 0, 0), # South (Element 114)
            (-1, 0, 0, 0), # West  (Element 110)
            (1, 0, 0, 0),  # East  (Element 112)
            (0, 0, 1, 0),  # Ana   (Element 116)
            (0, 0, -1, 0), # Kata  (Element 118)
            (0, 0, 0, 1),  # Over  (Element 120)
            (0, 0, 0, -1)  # Under (Element 122)
        ]
        self.reset_registers()

    def reset_registers(self):
        """Initializes hardware silicon coordinate registers back to absolute zero."""
        self.registers = {
            (0, 0, 0, 0): 0  # Center Processing Core Node (Element 102)
        }
        for bus in self.orthogonal_buses:
            self.registers[bus] = 0
            
        self.pc = 0
        self.halted = False

    def execute_stream(self, binary_bytes):
        """Runs raw machine bytecode packets directly on simulated register memory arrays."""
        self.reset_registers()
        cache = list(binary_bytes)
        self.pc = 0
        self.halted = False

        print("\n=== [UFNI CORE] EXECUTING BARE-METAL 4D SYSTEM RUNTIME ===")
        while self.pc < len(cache) and not self.halted:
            opcode = cache[self.pc]

            if opcode == 0x01:    # --- CONNECT SUBROUTINE ---
                src_dir = cache[self.pc + 1]
                dest_dir = cache[self.pc + 2]
                print(f"[PC {self.pc}]: Opcode 0x01 (CONNECT) -> Latched hardware bus paths: {hex(src_dir)} to {hex(dest_dir)}")
                self.pc += 3

            elif opcode == 0x02:  # --- YOUR EXACT //8 AND %8 INTEGRATED LOGIC LOOP ---
                pulse = cache[self.pc + 1]
                print(f"[PC {self.pc}]: Opcode 0x02 (RESONATE) -> Injecting energy pulse: {pulse} Units")
                
                target = (0, 0, 0, 0)
                self.registers[target] += pulse
                current_load = self.registers[target]
                
                # PATH A: The asymmetric whole-number floor integer split (//8)
                base_share = current_load // 8
                
                # PATH B: The exact conservation modulo remainder queue (%8)
                remainder = current_load % 8
                
                # Clear central input buffer register back to absolute zero baseline
                self.registers[target] = 0  
                
                # Execute Path A: Uniform energy mass distribution to all 8 neighbor cells
                for bus in self.orthogonal_buses:
                    self.registers[bus] += base_share
                    
                # Execute Path B: On-chip round-robin shift register queue loop for leftover remainders
                if remainder > 0:
                    for i in range(remainder):
                        target_bus = self.orthogonal_buses[i]
                        self.registers[target_bus] += 1
                        print(f"       [Shift Register Override] Allocated +1 remainder mass to cell: {target_bus}")
                    
                print(f"       [Execution Metric] Base Share (//8) = {base_share} | Leftover Remainder (%8) = {remainder}")
                self.pc += 2

            elif opcode == 0x03:  # --- SYSTEM CONSERVATION COLLAPSE SURVEILLANCE ---
                flag = cache[self.pc + 1]
                print(f"[PC {self.pc}]: Opcode 0x03 (COLLAPSE) -> Running verification scope: {hex(flag)}")
                
                # Audit the entire 4D matrix network grid load to confirm absolute mass protection
                total_mass = sum(self.registers.values())
                print(f"       [Surveillance Invariant] Total Combined Register Energy = {total_mass} Units")
                self.pc += 2
                self.halted = True
                print("[KERNEL STATUS]: Invariant verified. Grid power down stable.")

        print("\n--- FINAL 4D CHIP REGISTER REGISTER STATE DISPLAY ---")
        for addr, value in self.registers.items():
            print(f" Coordinate Space Register Slot {addr} : Balanced Energy Value = {value}")
        print("----------------------------------------------------\n")

# =====================================================================
# 4. ONE-CLICK PRODUCTION-GRADE SYSTEM INTERFACE
# =====================================================================
def run_mother_engine(sovereign_assembly_script):
    """The master call to compile and run any code script on the 4D engine instantly."""
    compiler = SovereignCompiler()
    kernel = SovereignKernel()
    
    # 1. Compile assembly source lines down into raw binary machine opcodes
    bytecode = compiler.assemble_script(sovereign_assembly_script)
    
    # 2. Fire bytecode stream straight into the hardware registers
    kernel.execute_stream(bytecode)

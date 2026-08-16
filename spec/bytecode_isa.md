# Sovereign-L Instruction Set Architecture (ISA) Specification v1.0

This document defines the low-level machine instruction byte mappings for the Sovereign-L bare-metal runtime environment. It completely eliminates floating-point decimal calculation drag by hard-gating execution paths directly inside hardware registers.

## 🔢 1. Core Opcode Binary Mapping Table

| Opcode Byte | Instruction | Operand Signature | Micro-Architectural Register Operation |
| :--- | :--- | :--- | :--- |
| `0x01` | **CONNECT** | `[Src_Dir] [Dest_Dir]` | Actively closes hardware circuit switches to bind two coordinate paths. Bypasses software virtual tables completely. |
| `0x02` | **RESONATE**| `[Pulse_Value]` | Fires the dual-path arithmetic MMU to execute whole-number floor division splits (`// 8`) and modulo remainder dispatching (`% 8`). |
| `0x03` | **COLLAPSE**| `[Scope_Flag]` | Performs a global register sum inventory check. Instantly trips an automated power kill-switch if energy conservation is violated. |

## 📐 2. Bounded Coordinate Directional Bytes
To restrict communication pathways to 8 orthogonal axial neighbors under the Manhattan L1 Norm Filter, relative address vectors are packed into discrete single bytes:

* `0x10` : Positive X-Axis Direction ($+X$)
* `0x11` : Negative X-Axis Direction ($-X$)
* `0x20` : Positive Y-Axis Direction ($+Y$)
* `0x21` : Negative Y-Axis Direction ($-Y$)
* `0x30` : Positive Z-Axis Direction ($+Z$)
* `0x31` : Negative Z-Axis Direction ($-Z$)
* `0x40` : Positive W-Axis Direction ($+W$)
* `0x41` : Negative W-Axis Direction ($-W$)

## 💾 3. Binary Packing Layout Rules
Instructions are processed as variable-length streams read directly from the binary instruction array:
1. **CONNECT Packing:** `[0x01] [Source_Byte] [Destination_Byte]` (Total 3 Bytes)
2. **RESONATE Packing:** `[0x02] [Unsigned_Integer_Value_Byte]` (Total 2 Bytes)
3. **COLLAPSE Packing:** `[0x03] [0xFF]` (Total 2 Bytes, where `0xFF` flags global scope check)

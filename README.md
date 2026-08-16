# sovereign-l-prototype
The low-level bare-metal runtime kernel execution environment and self-hosting compiler architecture for the Sovereign-L computing language.
# Sovereign-L Compiler & Bare-Metal Hardware Prototype

This repository houses the low-level, self-hosting compiler architecture and bare-metal runtime execution kernel for the **Sovereign-L** computing language. It implements the native hardware-level execution layer for the Unified Field Neuromorphic Intelligence (UFNI) framework.

## 🏛️ Architectural Hierarchy
By removing traditional operating system abstraction layers and virtual memory tables, Sovereign-L executes commands natively inside hardware registers using a discrete 4D whole-number coordinate matrix ($\mathbb{Z}^4$).

*   **`spec/bytecode_isa.md`**: The official Instruction Set Architecture (ISA) mapping text strings directly to machine binary tokens (`0x01`, `0x02`, `0x03`).
*   **`temporary_scaffold/`**: A temporary Python-based bootstrapping compiler used to generate the initial bare-metal binaries.
*   **`sovereign_source/`**: The true, self-hosting native compiler written entirely inside Sovereign-L syntax (`.sl`).
*   **`kernel/`**: The core hardware runtime loop executing whole-number memory adjustments without decimal arithmetic.

## 🔄 Self-Hosting Compilation Pipeline
[ native_compiler.sl ] ──► ( Compiled by bootstrap_compiler.py ) ──► [ independent_kernel.bin ]│▼ (Scaffold Deleted)[ New Source Code ]   ──► ( Compiled Natively by Kernel )       ──► [ Pure Machine Code ]
## 🔗 Cross-Link Core & Prior Art Validation
This prototype is an active technical continuation of the primary UFNI simulation framework. The underlying discrete mathematical theorems and structural layout claims are cryptographically timestamped and protected under global open-science infrastructure.

*   **Primary Theory Repository**: [unified-field-neuromorphic-intelligence](https://github.com/Sanket-20-22/unified-field-neuromorphic-intelligence)
*   **Permanent Reference DOI**: [https://doi.org](https://doi.org/10.5281/zenodo.21916505)
*   **Global Research Index**: OpenAIRE Active Tracking Ledger

## 📜 Intellectual Property Shield
This codebase is completely open-source and protected under the **GNU General Public License v3.0**. All derivative architectures, silicon layouts, or fork implementations are legally required to maintain open accessibility and provide absolute author attribution credit to: 

**Sanket Hazra (Jadavpur University)**

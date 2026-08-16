# Sovereign-L: An Exact Discrete Lattice Engine for Statistical Mechanics

This repository houses a bare-metal, whole-number execution core designed explicitly for computational physics simulations. By shifting the coordinate framework from continuous lines to a discrete four-dimensional integer matrix ($\mathbb{Z}^4$), this architecture completely eliminates floating-point truncation errors ($\epsilon$).

## 🌌 Core Physics Claims
*   **0.00% Rounding Loss:** Utilizing asymmetric whole-number floor division (`// 8`) and round-robin remainder loops (`% 8`) to guarantee absolute energy conservation over infinite processing cycles.
*   **Zero Approximation Drag:** Eliminating IEEE 754 floating-point mantissa tracking, reducing on-chip local data bus traffic overhead by 87.50%.
*   **Target Application:** Exact macro-state partition function tracking, localized vacuum field distribution models, and non-Euclidean quantum boundary simulations without decimal drift.

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

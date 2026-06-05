# AMT2ABC: From "Atomic Mechanism Triplets" to "Atomic Business Capabilities" — An Industrial Software Compiler

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**English** | [简体中文](./README.zh-CN.md)

---

**AMT2ABC** is an open-source ecosystem for compiling industrial software capabilities. It automatically compiles industrial mechanisms, expressed as Atomic Mechanism Triplets (**AMTs**), into reusable Atomic Business Capabilities (**ABCs**), enabling automated transformation from business goals to executable industrial applications.

> What industrial software lacks is not AI, but a Compiler.
> — AMT2ABC core thesis

## Why AMT2ABC?

Traditional industrial software development has long been trapped in a "project-based, siloed, costly-to-change" dilemma. Capabilities are hard to reuse across production lines and processes, and every change requires extensive manual code modification. Drawing on Huawei's Tau (τ) Law and the historical lessons of RISC + Compiler, AMT2ABC shifts complexity from low-level code to the instance-configuration layer, letting the system automatically understand business goals and compile recommended capability combinations.

## Core Concepts

| Concept | Full Name | Description |
|---------|-----------|-------------|
| **AMT** | Atomic Mechanism Triplet | The smallest irreducible industrial causal unit, e.g. "load ↑ → vibration ↑" |
| **SECP** | Structure, Event, Configuration, Process | The four-dimensional grammar of industrial software, providing unified structural labels for AMT |
| **ABC** | Atomic Business Capability | A minimum software capability unit that can be independently deployed and reused across scenarios |
| **Compiler** | AMT2ABC Compiler | The system that automatically extracts AMT Clusters from business goals (GS), packages them as ABCs, and orchestrates them into Apps/Agents |

## Architecture Overview

```
Working Domain → Mechanism → AMT → AMT Graph
                                           ↓
GS (Goal)  →  AMT Cluster  →  ABC
                                ↓
                  App/Agent → Scenario → OAO Loop
```

- **Human-defined parts**: Working Domain, Mechanism, AMT, AMT Graph
- **Compiler-automated parts**: GS → AMT Cluster → ABC → App/Agent

## Quick Start

### Prerequisites

- Basic understanding of industrial mechanisms
- Familiarity with YAML/JSON configuration

### Install the Compiler Prototype (MVP)

```bash
git clone https://github.com/zylliondata/AMT2ABC.git
cd AMT2ABC
# Detailed installation steps: docs/installation.md (coming soon)
```

### Minimal Example

Input goal: "Reduce porosity rate" (die-casting line)

Compiler outputs a recommended ABC combination (JSON example):

```json
{
  "goal": "Reduce porosity rate",
  "recommended_abc": ["Mold-Temperature Control ABC", "Shot-Speed Optimization ABC", "Vacuum Management ABC"]
}
```

For a full tutorial, see `docs/getting-started.md` (coming soon).

## Open-Source Roadmap

| Phase | Timeline | Goal |
|-------|----------|------|
| 1. Hands-on Prototype | This year Q3 | Open-source Compiler MVP + die-casting line example |
| 2. Community Contributions | This year Q4+ | Open contribution channels for AMT/SECP patterns |
| 3. ABC Registry | Next year | An ABC capability marketplace, similar to Docker Hub |
| 4. Standardization | Three years out | Domestic group standards → international standards |

## Contributing

We welcome contributions in all forms, including but not limited to:

- Submitting new AMT patterns or SECP fingerprints
- Packaging and sharing ABC modules
- Improving the Compiler's matching algorithm
- Improving documentation and tutorials

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed workflows.

## Code of Conduct

This project follows the Contributor Covenant Code of Conduct. Please read the [full text](CODE_OF_CONDUCT.md).

## Security

To report a security vulnerability, please follow the process in [SECURITY.md](SECURITY.md).

## License

[Apache 2.0 License](LICENSE) © AMT2ABC Contributors

## Contact

- Issues: <https://github.com/zylliondata/AMT2ABC/issues>
- Discussions: <https://github.com/zylliondata/AMT2ABC/discussions>
- Email: info@zylliondata.com

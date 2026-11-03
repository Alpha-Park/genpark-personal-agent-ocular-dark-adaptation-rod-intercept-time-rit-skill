# Ocular Dark Adaptation Rod Intercept Time (RIT) Skill

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://www.python.org/)
[![OpenClaw](https://img.shields.io/badge/ecosystem-OpenClaw-orange.svg)](https://openclaw.org/)
[![GenPark](https://img.shields.io/badge/sovereign-GenPark-purple.svg)](https://alphapark.ai/)
[![MCP](https://img.shields.io/badge/protocol-MCP-success.svg)](https://modelcontextprotocol.io/)

Retinal Dark Adaptation Kinetics and Rod Intercept Time (RIT) Quantitative Evaluator based on scotopic psychophysical modeling.

```mermaid
flowchart TD
    A[Post-Bleach Luminance Sensitivity Curve] --> B[Kohlrausch Bend Rod-Cone Break Detection]
    B --> C[Rod Branch Exponential Deceleration]
    C --> D[Standard Criterion Threshold Crossing]
    D --> E[Rod Intercept Time RIT in Minutes]
    E --> F[Retinoid Cycle & Bruch Membrane Health Guidance]
```

## Features
- **Zero PIP Dependencies**: Implemented strictly with Python Standard Library (`math`, `json`, `sys`, `typing`).
- **Biphasic Retinal Modeling**: Distinguishes cone photopic plateau from rod rhodopsin regeneration.
- **RIT Quantitation**: Standard clinical dark adaptometry metric for early nyctalopia and macular screening.
- **Dual Architecture**: Native Python import and Model Context Protocol (MCP) JSON-RPC 2.0 stdio server.

## Quickstart
```bash
python example_usage.py
```

## License
Apache-2.0

# Metadrive-Scenario

This repo contains scenarios from different sources for training and testing autonomous vehicles.
All scenarios can be runned in [MetaDrive Simulator](https://github.com/metadriverse/metadrive), where various sensor
inpurt can be retrieved for making driving decisions. Until now, we provide three types of driving scenarios:

- **Synthetic Scenarios**: Maps are generated via Procedural Generation (PG). Traffic vehicles are generated and 
controlled according to manually desigened rules
- **Real Scenarios**: These scenarios are built on [Waymo motion dataset](https://waymo.com/open/). Maps and surrounding 
vehicles are collected and recorded in real world.
- **Generated Scenarios**: Empowered by [TrafficGen](https://metadriverse.github.io/trafficgen/), new traffic flow can
be generated and resemble the real world traffic scenarios given a real-world map.

## 🛠 Quick Start
**Prerequisite**: Installing MetaDrive via:

```bash
# minimal version requirement is metadrive-0.2.6. For any installation issues, please refer to Metadrive: https://github.com/metadriverse/metadrive.
pip install "metadrive-simulator>=0.2.6"
```

**MetaDrive-Scenario Installation**:

```bash
git clone git@github.com:metadriverse/metadrive-scenario.git
cd metadrive-scenario
pip install -e .
```

**Dataset Download**:
1. Download data from https://github.com/metadriverse/metadrive-scenario/releases.
2. Place data under ```metadrive-scenario/metadrive_scenario/dataset```

## 🚕 Examples

LQY(TBD)
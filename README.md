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

We provide an example:```metadrive_scenario/examples/run_scenarios.py```, where basic usage and APIs are shown.
For driving in the **synthetic scenarios**, run:
```bash
python metadrive_scenario/examples/run_scenarios.py  --dataset env_num_3000_start_seed_0_synthetic --scenario_start=0 --scenario_end=3000 
```

For driving in the **real Waymo scenarios**, run:
```bash
python metadrive_scenario/examples/run_scenarios.py  --dataset env_num_1175_waymo --scenario_start=0 --scenario_end=1000 
```
The scenarios will be built by replaying collected surrounding vehicles' trajectories, while you can add argument 
```--idm_traffic``` to turn these vehicles into reactive ones.

For both scenario types, you can add the optional argument ```--manual_control``` to control the vehicle via ```w```, ```a```, ```s```, ```d```.
Also, you can add another argumane ```--topdown``` to use 2-D birdeye-view renderer, which is built with pygame.


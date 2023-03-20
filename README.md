# Metadrive-Scenario

This repo contains diverse traffic scenarios for evaluating autonomous vehicles in simulation.
All scenarios are reactive and can be ran in [MetaDrive Simulator](https://github.com/metadriverse/metadrive). 

![teaser](./docs/teaser.gif)

Currently we provide three sources of traffic scenarios:
- **Synthetic Scenarios**: Maps are generated via Procedural Generation (PG). Traffic vehicles are generated and 
controlled according to rules
    ```
    Synthetic Dataset Statistics:
      Number of scenarios: 3000
      Number of traffic vehicles per scene: 8.9±3.1
      Block Distrubution:
        Curve: 0.156
        Straight: 0.331
        Roundabout: 0.077
        T-intersection: 0.074
        Intersection: 0.077
        Ramp (merge): 0.081
        Ramp (diverge): 0.076
        Bottleneck (merge): 0.065
        Bottleneck (diverge): 0.068
    ```
- **Real-world Scenarios**: These scenarios are built from [Waymo motion dataset](https://waymo.com/open/). Maps and surrounding vehicles are collected and recorded in real world.
    ```
    Real-world Dataset Statistics:
      Number of scenarios: 1165
      Number of traffic vehicles per scene: 26.1±21.5
    ```
- **Generated Scenarios**: Empowered by our generative model [TrafficGen](https://metadriverse.github.io/trafficgen/), new traffic flow can be generated and resembles the real-world data given a HD map.

## 🛠 Quick Start
**Prerequisite**: Install MetaDrive first via:

```bash
git clone https://github.com/metadriverse/metadrive.git
cd metadrive
pip install -e .
```

**MetaDrive-Scenario Installation**:

```bash
git clone git@github.com:metadriverse/metadrive-scenario.git
cd metadrive-scenario
pip install -e .
```

**Download Dataset**:
1. Download data from https://github.com/metadriverse/metadrive-scenario/releases.
2. Place data under ```metadrive-scenario/metadrive_scenario/dataset```

## 🚕 Examples

We provide an example script:```metadrive_scenario/examples/run_scenarios.py```, where basic usage and APIs are described.
For driving in the **synthetic scenarios**, run:
```bash
python metadrive_scenario/examples/run_scenarios.py  --dataset env_num_3000_start_seed_0_synthetic --scenario_start=0 --scenario_end=3000 
```

For driving in the **real-world Waymo scenarios**, run:
```bash
python metadrive_scenario/examples/run_scenarios.py  --dataset env_num_1165_waymo --scenario_start=0 --scenario_end=1000 
```
The scenarios will be built by replaying collected surrounding vehicles' trajectories, while you can add argument 
```--idm_traffic``` to turn these vehicles into reactive ones.

For both scenario types, you can add the optional argument ```--manual_control``` to control the vehicle via ```w```, ```a```, ```s```, ```d```.
Also, you can add another argumane ```--topdown``` to use 2-D birdeye-view renderer, which is built with pygame.


## Training

Install Ray for RL training:

```bash
pip install ray==2.2.0
pip install ray[rllib]==2.2.0
pip install tensorflow_probability  # Not used

# Install pytorch by yourself. We use:
conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia


```

## 🏫 Documentation

Refer to Documentation of [MetaDrive](https://metadrive-simulator.readthedocs.io) for detail.


## 📎 References

If you use MetaDrive in your own work, please cite:

```latex
@article{li2022metadrive,
  title={Metadrive: Composing diverse driving scenarios for generalizable reinforcement learning},
  author={Li, Quanyi and Peng, Zhenghao and Feng, Lan and Zhang, Qihang and Xue, Zhenghai and Zhou, Bolei},
  journal={IEEE Transactions on Pattern Analysis and Machine Intelligence},
  year={2022}
}
```


import pickle

from metadrive_scenario.data_generation import SYNTHETIC_DATA_CONFIG
import numpy as np
from metadrive.envs.metadrive_env import MetaDriveEnv
import os
from tqdm import tqdm
from metadrive_scenario import METADRIVE_SCENARIO_DATASET_DIR, DataType
from metadrive.policy.idm_policy import IDMPolicy


def vis_synthetic_data(env_num, start_seed):
    """
    Generate synthetic data
    """
    SYNTHETIC_DATA_CONFIG.update({"environment_num": env_num,
                                  "start_seed": start_seed,
                                  "use_render": True,
                                  "agent_policy": IDMPolicy,
                                  "record_episode": True})
    env = MetaDriveEnv(SYNTHETIC_DATA_CONFIG)
    env.reset()
    scenarios = {}
    stat = {"traffic_vehicle_num": []}
    total_block_num = 0
    for seed in tqdm(range(start_seed, start_seed + env_num), desc="Generate Scenarios"):
        env.reset(force_seed=seed)
        for i in range(1000):
            o, r, d, i = env.step([0, 1])
            env.render(text={"seed": env.current_seed})
            if d:
                break
    env.close()


if __name__ == "__main__":
    # generate_synthetic_data(env_num=20, start_seed=0,dataset_name="test.pkl")
    vis_synthetic_data(env_num=20, start_seed=0)

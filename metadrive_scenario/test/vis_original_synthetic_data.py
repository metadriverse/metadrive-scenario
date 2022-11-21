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
    SYNTHETIC_DATA_CONFIG.update(
        {
            "environment_num": 1,
            "start_seed": 1,
            'traffic_density': 0.,
            "use_render": True,
            "manual_control": True,
            "agent_policy": None,
            "map": "XXXXX",
            "record_episode": False
        }
    )
    env = MetaDriveEnv(SYNTHETIC_DATA_CONFIG)
    env.reset()
    scenarios = {}
    stat = {"traffic_vehicle_num": []}
    total_block_num = 0
    for seed in tqdm(range(start_seed, start_seed + env_num), desc="Generate Scenarios"):
        env.reset()
        for i in range(1000):
            o, r, d, i = env.step([0, 1])
            env.render(
                text={
                    "seed": env.current_seed,
                    "dist_left:": env.vehicle.dist_to_left_side,
                    "dist_right:": env.vehicle.dist_to_right_side,
                    "ref_lane": env.vehicle.navigation.current_ref_lanes[0],
                }
            )
            if d:
                break
    env.close()


if __name__ == "__main__":
    # generate_synthetic_data(env_num=20, start_seed=0,dataset_name="test.pkl")
    vis_synthetic_data(env_num=20, start_seed=0)

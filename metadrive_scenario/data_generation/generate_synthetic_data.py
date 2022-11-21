import pickle

from metadrive_scenario.data_generation import SYNTHETIC_DATA_CONFIG
import numpy as np
from metadrive.envs.metadrive_env import MetaDriveEnv
import os
from tqdm import tqdm
from metadrive_scenario import METADRIVE_SCENARIO_DATASET_DIR, DataType


def generate_synthetic_data(env_num, start_seed, dataset_name=None):
    """
    Generate synthetic data
    """
    dataset_name = dataset_name or "env_num_{}_start_seed_{}_synthetic.pkl".format(env_num, start_seed)
    if ".pkl" not in dataset_name:
        dataset_name += ".pkl"
    dataset_name = os.path.join(METADRIVE_SCENARIO_DATASET_DIR, dataset_name)
    SYNTHETIC_DATA_CONFIG.update({"environment_num": env_num, "start_seed": start_seed, "record_episode": True})
    env = MetaDriveEnv(SYNTHETIC_DATA_CONFIG)
    env.reset()
    scenarios = {}
    stat = {"traffic_vehicle_num": []}
    total_block_num = 0
    for seed in tqdm(range(start_seed, start_seed + env_num), desc="Generate Scenarios"):
        env.reset(force_seed=seed)
        data = env.engine.record_manager.get_episode_metadata()
        scenarios[seed] = data
        # stat
        traffic_num = len(env.engine.traffic_manager.vehicles)
        stat["traffic_vehicle_num"].append(traffic_num)
        map = data["map_data"]
        for block_config in map["block_sequence"]:
            total_block_num += 1
            if block_config["id"] in stat:
                stat[block_config["id"]] += 1
            else:
                stat[block_config["id"]] = 0
    for k, v in stat.items():
        if k != "traffic_vehicle_num":
            stat[k] = v / total_block_num
        else:
            traffic_num = stat[k].copy()
            stat[k] = {"mean": np.mean(traffic_num), 'std': (np.std(traffic_num))}
    with open(dataset_name, "wb+") as file:
        dataset = {
            "scenarios": scenarios,
            "stat": stat,
            "env_class": MetaDriveEnv,
            "config": scenarios[0]["global_config"]
        }
        pickle.dump(dataset, file)
    print(stat)
    env.close()


if __name__ == "__main__":
    generate_synthetic_data(env_num=3000, start_seed=0)

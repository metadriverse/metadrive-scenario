from metadrive_scenario.data_generation import SYNTHETIC_DATA_CONFIG
from metadrive.envs.metadrive_env import MetaDriveEnv
import os
from metadrive_scenario import METADRIVE_SCENARIO_DATASET_DIR, DataType


def generate_synthetic_data(env_num, start_seed):
    """
    Generate synthetic data
    """
    SYNTHETIC_DATA_CONFIG.update({"environment_num": env_num,
                                  "start_seed": start_seed})
    env = MetaDriveEnv(SYNTHETIC_DATA_CONFIG)
    env.reset()
    data = env.engine.map_manager.dump_all_maps(
        file_name=os.path.join(METADRIVE_SCENARIO_DATASET_DIR,
                               "{}_env_num_{}_start_seed_{}.pkl".format(DataType.SYNTHETIC, env_num, start_seed)))

    stat = {}
    total_block_num = 0
    for map in data.values():
        for block_config in map["block_sequence"]:
            total_block_num += 1
            if block_config["id"] in stat:
                stat[block_config["id"]] += 1
            else:
                stat[block_config["id"]] = 0
    for k, v in stat.items():
        stat[k] = v / total_block_num
    print(stat)
    env.close()


if __name__ == "__main__":
    generate_synthetic_data(env_num=20, start_seed=0)

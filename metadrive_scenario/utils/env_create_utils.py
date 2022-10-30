import os.path as osp
from metadrive_scenario import METADRIVE_SCENARIO_DATASET_DIR, DataType
from metadrive_scenario.data_generation.generate_synthetic_data import SYNTHETIC_DATA_CONFIG

from metadrive.envs.metadrive_env import MetaDriveEnv


def parse_dataset_name(dataset_name):
    if dataset_name.rfind(".pkl") == -1:
        dataset_name += ".pkl"
    data_path = osp.join(METADRIVE_SCENARIO_DATASET_DIR, dataset_name)
    assert osp.exists(data_path), "Can not find dataset: {}".format(
        dataset_name)
    if DataType.SYNTHETIC in dataset_name:
        env_cls = MetaDriveEnv
        dataset_name = dataset_name[:-4]
        env_num_str = "_env_num_"
        start_seed_str = "_start_seed_"
        idx_env_num = dataset_name.find(env_num_str)
        idx_start_seed = dataset_name.find(start_seed_str)
        env_num = int(dataset_name[idx_env_num + len(env_num_str): idx_start_seed])
        start_seed = int(dataset_name[idx_start_seed + len(start_seed_str):])
        env_config = SYNTHETIC_DATA_CONFIG.copy()
        env_config["start_seed"] = start_seed
        env_config["environment_num"] = env_num
        return env_cls, env_config, data_path
    else:
        raise ValueError("Don't support {}".format(dataset_name))


def create_env(dataset_name):
    env_cls, env_config, full_data_path = parse_dataset_name(dataset_name)
    env = env_cls(env_config)
    env.reset()
    env.engine.map_manager.load_all_maps(full_data_path)
    env.reset()
    return env


if __name__ == "__main__":
    env = create_env("synthetic_env_num_20_start_seed_0")
    env.reset()

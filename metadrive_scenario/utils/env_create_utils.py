import logging
from metadrive.engine.engine_utils import engine_initialized
from metadrive.utils.config import Config
import copy
import os.path as osp
import pickle
import numpy as np
from metadrive_scenario import METADRIVE_SCENARIO_DATASET_DIR
import json
import gym

SCENARIO_CONFIG = {"dataset_path": None,
                   "scenario_start": None,
                   "scenario_end": None,
                   "seed": None}


class MetaDriveScenario(gym.Env):
    def __init__(self, config=None):
        """
        :param env: env to wrap
        :param scenarios: scenario dataset
        :param scenario_start: scenario start index (inclusive)
        :param scenario_end: scenario end index (exclusive)
        :param seed: random seed for determing random choosing scenario
        """

        self.wrapper_config = config or SCENARIO_CONFIG
        data_path = config["dataset_path"]
        assert osp.exists(data_path), "Can not find dataset: {}".format(data_path)
        with open(data_path, "rb+") as file:
            self.dataset = dataset = pickle.load(file)

        env_class = dataset["env_class"]
        env_config = dataset["config"]
        env_config["record_episode"] = False
        env_config["replay_episode"] = None
        env_config["only_reset_when_replay"] = True
        env_config.update(config["extra_env_config"])
        env_config["target_vehicle_configs"] = {}  # this will be filled automatically

        self._env = env_class(copy.deepcopy(env_config))
        self._scenarios = scenarios = self.dataset["scenarios"]
        self._random_seed_for_wrapper = config["seed"]
        self.scenario_start = config["scenario_start"] or min(list(scenarios.keys()))
        assert self.scenario_start >= min(list(scenarios.keys())), \
            "Scenario range error! start; {}".format(self.scenario_start)
        self.scenario_end = config["scenario_end"] or max(list(scenarios.keys())) + 1
        assert self.scenario_end <= max(list(scenarios.keys())) + 1, \
            "Scenario range error! end: {}".format(self.scenario_end)
        self._np_random = np.random.RandomState(self._random_seed_for_wrapper)
        self.log_info(copy.deepcopy(env_config))

    def __getattr__(self, item):
        if item not in ["reset", "step", "render", "close", "seed"]:
            # for overriding the gym.Env
            return self._env.__getattribute__(item)
        else:
            return self.__getattribute__(item)

    def step(self, *args, **kwargs):
        return self._env.step(*args, **kwargs)

    def render(self, *args, **kwargs):
        return self._env.render(*args, **kwargs)

    def close(self):
        self._env.close()

    def seed(self, seed=None):
        self._random_seed_for_wrapper = seed
        self._np_random = np.random.RandomState(seed)

    @property
    def observation_space(self):
        return self._env.observation_space

    @property
    def action_space(self):
        return self._env.action_space

    def reset(self, seed=None):
        intialize_before_reset = engine_initialized()
        if seed is None:
            seed = self._np_random.randint(self.scenario_start, self.scenario_end)
            scenario = copy.deepcopy(self._scenarios[seed])
        else:
            assert isinstance(seed, int) and self.scenario_start <= seed and self.scenario_end, "seed error!"
            scenario = copy.deepcopy(self._scenarios[seed])
        self._env.config["replay_episode"] = scenario
        self._env.config["record_scenario"] = False
        self._env.config["only_reset_when_replay"] = True
        ret = self._env.reset(force_seed=seed)
        if not intialize_before_reset:
            # Now engine is initilaized run callback function
            self.after_initialize()
        return ret

    def after_initialize(self):
        self._env.engine.accept("r", self.reset)

    def log_info(self, env_config):
        if isinstance(env_config, Config):
            env_config = env_config.get_dict()
        if "block_dist_config" in env_config:
            env_config["block_dist_config"] = env_config["block_dist_config"].get_config()
        print("Load Dataset: {}".format(self.wrapper_config["dataset_path"]))
        print("Dataset Features: {}".format(json.dumps(self.dataset["stat"], indent=4)))
        print("Environment Config: \n {}".format(json.dumps(env_config, indent=4)))
        print("Index Range: {}-{}".format(self.scenario_start, self.scenario_end))


def key_check(data_1, data_2):
    assert isinstance(data_1, dict) and isinstance(data_2, dict), "Only Dict type can be checked"
    intersect = set(data_1.keys()).intersection(set(data_2.keys()))
    if len(intersect) > 0:
        logging.info("{} in the config will be overwritten with {}".format([(i, data_1[i]) for i in intersect],
                                                                           [(i, data_2[i]) for i in intersect]))


def create_env_and_config(dataset_name, scenario_start=None, scenario_end=None, extra_env_config=None, seed=0):
    extra_env_config = extra_env_config or {}
    if dataset_name.rfind(".pkl") == -1:
        dataset_name += ".pkl"
    data_path = osp.join(METADRIVE_SCENARIO_DATASET_DIR, dataset_name)
    config = dict(dataset_path=data_path,
                  scenario_start=scenario_start,
                  scenario_end=scenario_end,
                  seed=seed,
                  extra_env_config=extra_env_config)
    return MetaDriveScenario, config


if __name__ == "__main__":
    env_class, config = create_env_and_config("env_num_20_start_seed_0_synthetic",
                                              extra_env_config={"use_render": True, "manual_control": True})
    env = env_class(config)
    print(env.observation_space)
    print(env.action_space)
    env.reset()
    for i in range(20):
        env.reset(seed=i)
        for t in range(100):
            o, r, d, i = env.step([0, 1])
            env.render(text={"seed": env.current_seed})
            # print(env.vehicle.position)
            if d:
                break

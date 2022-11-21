import logging
from metadrive.envs.metadrive_env import MetaDriveEnv
from metadrive.envs.real_data_envs.waymo_idm_env import WaymoIDMEnv
from metadrive.engine.engine_utils import engine_initialized
from metadrive.utils.config import Config
import copy
import os.path as osp
import pickle
import numpy as np
from metadrive_scenario import METADRIVE_SCENARIO_DATASET_DIR
import json
import gym

SCENARIO_CONFIG = {
    "dataset_path": None,
    "scenario_start": None,
    "scenario_end": None,
    "seed": None,
    "waymo_env": False,
    "random_set_seed": True
}


class MetaDriveScenario(gym.Env):
    def __init__(self, config=None):
        """
        :param env: env to wrap
        :param scenarios: scenario dataset
        :param scenario_start: scenario start index (inclusive)
        :param scenario_end: scenario end index (exclusive)
        :param seed: random seed for determing random choosing scenario
        """
        if config is not None:
            self.wrapper_config = SCENARIO_CONFIG
            self.wrapper_config.update(config)
        self._waymo_env = config["waymo_env"]
        data_path = config["dataset_path"]
        assert osp.exists(data_path), "Can not find dataset: {}".format(data_path)

        if not self._waymo_env:
            with open(data_path, "rb+") as file:
                self.dataset = dataset = pickle.load(file)
            env_class = dataset["env_class"]
            env_config = dataset["config"]
            env_config["record_episode"] = False
            env_config["replay_episode"] = None
            env_config["only_reset_when_replay"] = True
            env_config.update(self.wrapper_config["extra_env_config"])
            env_config["target_vehicle_configs"] = {}  # this will be filled automatically
            self._scenarios = scenarios = self.dataset["scenarios"]
            self.scenario_start = self.wrapper_config["scenario_start"] or min(list(scenarios.keys()))
            assert self.scenario_start >= min(list(scenarios.keys())), \
                "Scenario range error! start; {}".format(self.scenario_start)
            self.scenario_end = self.wrapper_config["scenario_end"] or max(list(scenarios.keys())) + 1
            assert self.scenario_end <= max(list(scenarios.keys())) + 1, \
                "Scenario range error! end: {}".format(self.scenario_end)
            self._env = env_class(copy.deepcopy(env_config))
        else:
            env_config = WaymoIDMEnv.default_config().get_dict()
            env_config["waymo_data_directory"] = data_path
            self.scenario_start = self.wrapper_config["scenario_start"]
            assert self.scenario_start is not None, "This can not be determined automatically!"
            self.scenario_end = self.wrapper_config["scenario_end"]
            assert self.scenario_end is not None, "This can not be determined automatically!"
            env_config["start_case_index"] = self.scenario_start
            env_config["case_num"] = self.scenario_end - self.scenario_start
            # the data check will be finished by metadrive automatically
            env_config.update(self.wrapper_config["extra_env_config"])
            self._env = WaymoIDMEnv(env_config)
            self.dataset = None
            self._scenarios = None
        self.log_data_info(copy.deepcopy(env_config))

        self._random_set_seed = self.wrapper_config["random_set_seed"]
        self._random_seed_for_wrapper = self.wrapper_config["seed"]
        self._np_random = np.random.RandomState(self._random_seed_for_wrapper)
        self._env_seed = self.scenario_start

    # def __getattr__(self, item):
    #     try:
    #         ret = self.__getattribute__(item)
    #     except AttributeError:
    #         try:
    #         ret = self._env.__getattribute__(item)
    #     return ret

    @property
    def current_seed(self):
        return self._env.current_seed

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
            scenario = copy.deepcopy(self._scenarios[self._env_seed]) if not self._waymo_env else None
            seed = self._env_seed
            if self._random_set_seed:
                self._env_seed = self._np_random.randint(self.scenario_start, self.scenario_end)
            else:
                self._env_seed += 1
                if self._env_seed >= self.scenario_end:
                    self._env_seed = self.scenario_start

        else:
            assert isinstance(seed, int) and self.scenario_start <= seed and self.scenario_end, "seed error!"
            scenario = copy.deepcopy(self._scenarios[seed]) if not self._waymo_env else None
        if not self._waymo_env:
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

    def log_data_info(self, env_config):
        if isinstance(env_config, Config):
            env_config = env_config.get_dict()
        if "block_dist_config" in env_config and not self._waymo_env:
            env_config["block_dist_config"] = env_config["block_dist_config"].get_config()
        print("Load Dataset: {}".format(self.wrapper_config["dataset_path"]))
        print("Index Range: {}-{}".format(self.scenario_start, self.scenario_end))
        # print("Environment Config: \n {}".format(pickle.dumps(env_config)))
        if not self._waymo_env:
            print("Dataset Features: {}".format(json.dumps(self.dataset["stat"], indent=4)))


def key_check(data_1, data_2):
    assert isinstance(data_1, dict) and isinstance(data_2, dict), "Only Dict type can be checked"
    intersect = set(data_1.keys()).intersection(set(data_2.keys()))
    if len(intersect) > 0:
        logging.info(
            "{} in the config will be overwritten with {}".format(
                [(i, data_1[i]) for i in intersect], [(i, data_2[i]) for i in intersect]
            )
        )


def create_env_and_config(
    dataset_path,
    scenario_start=None,
    scenario_end=None,
    extra_env_config=None,
    random_set_seed_when_reset=False,
    random_seed=0,
    waymo_env=False,
):
    extra_env_config = extra_env_config or {}
    if dataset_path.rfind(".pkl") == -1 and not waymo_env:
        dataset_path += ".pkl"
    data_path = osp.join(METADRIVE_SCENARIO_DATASET_DIR, dataset_path)
    config = dict(
        dataset_path=data_path,
        scenario_start=scenario_start,
        scenario_end=scenario_end,
        seed=random_seed,
        waymo_env=waymo_env,
        extra_env_config=extra_env_config,
        random_set_seed=random_set_seed_when_reset
    )
    return MetaDriveScenario, config


if __name__ == "__main__":
    env_class, config = create_env_and_config(
        "env_num_20_start_seed_0_synthetic",
        extra_env_config={
            "use_render": True,
            "manual_control": True
        },
        scenario_start=10,
        scenario_end=15
    )
    env = env_class(config)
    print(env.observation_space)
    print(env.action_space)
    env.reset()
    for i in range(20):
        env.reset()
        for t in range(10000):
            o, r, d, i = env.step([0, 1])
            env.render(text={"seed": env.current_seed})
            # print(env.vehicle.position)
            if d:
                break

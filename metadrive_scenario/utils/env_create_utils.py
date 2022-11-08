import logging
import copy
import os.path as osp
import pickle
import numpy as np
from metadrive_scenario import METADRIVE_SCENARIO_DATASET_DIR


class MetaDriveScenario:
    def __init__(self, env, scenarios, scenario_start=None, scenario_end=None, seed=0):
        """
        :param env: env to wrap
        :param scenarios: scenario dataset
        :param scenario_start: scenario start index inclusive)
        :param scenario_end: scenario end index exclusive)
        :param seed: random seed for determing random choosing scenario
        """
        self._env = env
        self._scenarios = scenarios
        self._random_seed_for_wrapper = 0
        self.scenario_start = scenario_start or min(list(scenarios.keys()))
        assert self.scenario_start >= min(list(scenarios.keys())), "Scenario range error!"
        self.scenario_end = scenario_end or max(list(scenarios.keys()))
        assert self.scenario_end < max(list(scenarios.keys())) + 1, "Scenario range error!"
        self.reset()
        self._env.engine.accept("r", self.reset)

    def __getattr__(self, item):
        if item != "reset":
            return self._env.__getattribute__(item)

    def reset(self, seed=None):
        if seed is None:
            seed = np.random.RandomState(self._random_seed_for_wrapper).randint(self.scenario_start, self.scenario_end)
            scenario = copy.deepcopy(self._scenarios[seed])
        else:
            assert isinstance(seed, int) and self.scenario_start <= seed and self.scenario_end, "seed error!"
            scenario = copy.deepcopy(self._scenarios[seed])
        self._env.config["replay_episode"] = scenario
        self._env.config["record_scenario"] = False
        self._env.config["only_reset_when_replay"] = True
        return self._env.reset(force_seed=seed)


def key_check(data_1, data_2):
    assert isinstance(data_1, dict) and isinstance(data_2, dict), "Only Dict type can be checked"
    intersect = set(data_1.keys()).intersection(set(data_2.keys()))
    if len(intersect) > 0:
        logging.info("{} in the config will be overwritten with {}".format([(i, data_1[i]) for i in intersect],
                                                                           [(i, data_2[i]) for i in intersect]))


def create_env(dataset_name, scenario_start=None, scenario_end=None, extra_env_config=None):
    extra_env_config = extra_env_config or {}
    if dataset_name.rfind(".pkl") == -1:
        dataset_name += ".pkl"
    data_path = osp.join(METADRIVE_SCENARIO_DATASET_DIR, dataset_name)
    assert osp.exists(data_path), "Can not find dataset: {}".format(dataset_name)
    with open(data_path, "rb+") as file:
        dataset = pickle.load(file)
    env_class = dataset["env_class"]
    config = dataset["config"]
    config["record_episode"] = False
    config["replay_episode"] = None
    config["only_reset_when_replay"] = True
    config.update(extra_env_config)
    env = MetaDriveScenario(env_class(config),
                            scenarios=dataset["scenarios"],
                            scenario_start=scenario_start,
                            scenario_end=scenario_end)
    print("Load Dataset: {}".format(data_path))
    print("Environment Config: {}".format(config))
    print("Index Range: {}-{}".format(env.scenario_start, env.scenario_end))
    print("Dataset Features: {}".format(dataset["stat"]))
    return env


if __name__ == "__main__":
    env = create_env("test_env_num_20_start_seed_0_synthetic",
                     extra_env_config={"use_render": True, "manual_control": True})
    env.reset()
    for i in range(20):
        env.reset(seed=i)
        for t in range(100):
            o, r, d, i = env.step([0, 1])
            print(env.vehicle.position)
            if d:
                break

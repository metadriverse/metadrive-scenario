from metadrive_scenario.utils.env_create_utils import create_env_and_config
from metadrive.policy.idm_policy import IDMPolicy


def test_seed_synthetic():
    env_class, config = create_env_and_config("env_num_3000_start_seed_0_synthetic",
                                              extra_env_config={"use_render": False, "manual_control": False,
                                                                "agent_policy": None},
                                              random_set_seed_when_reset=False)
    # env.reset()
    env = env_class(config)
    for i in range(100, 3100):
        env.reset()
        assert env.current_seed == i - 100, env.current_seed

    env.close()

    env_class, config = create_env_and_config("env_num_20_start_seed_0_synthetic",
                                              extra_env_config={"use_render": False, "manual_control": False,
                                                                "agent_policy": None},
                                              random_set_seed_when_reset=False,
                                              scenario_end=17,
                                              scenario_start=10)
    # env.reset()
    env = env_class(config)
    for i in range(110, 117):
        env.reset()
        assert 10 <= env.current_seed < 17


def test_seed_waymo():
    env_class, config = create_env_and_config("1000_waymo_training",
                                              extra_env_config={"use_render": False, "manual_control": False,
                                                                "agent_policy": None},
                                              scenario_start=0,
                                              waymo_env=True,
                                              scenario_end=1000,
                                              random_set_seed_when_reset=False)
    # env.reset()
    env = env_class(config)
    for i in range(100, 1100):
        try:
            env.reset()
        except Exception as e:
            print(e)
            print("Error Seed:", env.current_seed)
            raise ValueError
        assert env.current_seed == i - 100, env.current_seed

    env.close()

    env_class, config = create_env_and_config("1000_waymo_training",
                                              extra_env_config={"use_render": False, "manual_control": False,
                                                                "agent_policy": None},
                                              random_set_seed_when_reset=False,
                                              scenario_end=123,
                                              waymo_env=True,
                                              scenario_start=10)
    # env.reset()
    env = env_class(config)
    for i in range(10, 124):
        env.reset()
        assert 10 <= env.current_seed < 17


if __name__ == "__main__":
    test_seed_waymo()

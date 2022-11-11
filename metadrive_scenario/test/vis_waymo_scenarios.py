from metadrive_scenario.utils.env_create_utils import create_env_and_config
from metadrive.policy.idm_policy import IDMPolicy

if __name__ == "__main__":
    env_class, config = create_env_and_config("1000_waymo_training",
                                              extra_env_config={"use_render": True, "manual_control": False},
                                              random_set_seed_when_reset=False,
                                              scenario_start=0,
                                              waymo_env=True,
                                              scenario_end=1000)
    env = env_class(config)
    for i in range(10000):
        env.reset()
        for t in range(1000):
            o, r, d, i = env.step([0, 1])
            env.render(text={"seed": env.current_seed})
            if d:
                break

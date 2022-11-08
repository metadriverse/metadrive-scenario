from metadrive_scenario.utils.env_create_utils import create_env
from metadrive.policy.idm_policy import IDMPolicy

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

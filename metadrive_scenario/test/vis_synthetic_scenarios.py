from metadrive_scenario.utils.env_create_utils import create_env
from metadrive.policy.idm_policy import IDMPolicy

if __name__ == "__main__":
    env_class, config = create_env("env_num_20_start_seed_0_synthetic",
                     extra_env_config={"use_render": True, "manual_control": False, "agent_policy":IDMPolicy})
    # env.reset()
    env = env_class(config)
    for i in range(9,20):
        env.reset()
        for t in range(1000):
            o, r, d, i = env.step([0, 1])
            env.render(text={"seed":env.current_seed})
            # print(env.vehicle.position)
            if d:
                break

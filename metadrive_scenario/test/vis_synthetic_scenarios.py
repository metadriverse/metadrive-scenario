from metadrive_scenario.utils.env_create_utils import create_env
from metadrive.policy.idm_policy import IDMPolicy

if __name__ == "__main__":
    config = {"use_render": True,
              "traffic_density": 0.2,
              "agent_policy": IDMPolicy,
              "manual_control": True}
    env = create_env("synthetic_env_num_20_start_seed_0", config=config)
    env.reset(force_seed=6)
    while True:
        o, r, d, i = env.step(env.action_space.sample())
        # env.render(text={"seed": env.current_seed})
        if d:
            env.reset(force_seed=6)

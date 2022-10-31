from metadrive_scenario.utils.env_create_utils import create_env

if __name__ == "__main__":
    config = {"use_render": True,
              "traffic_density": 0.2,
              "manual_control": True}
    env = create_env("synthetic_env_num_3000_start_seed_0", config=config)
    env.reset()
    while True:
        env.step(env.action_space.sample())
        env.render(text={"seed": env.current_seed})

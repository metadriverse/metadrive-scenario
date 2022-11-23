from metadrive_scenario.utils.env_create_utils import create_env_and_config
from metadrive.policy.idm_policy import IDMPolicy
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--manual_control", action="store_true")
    parser.add_argument("--scenario_start", type=int, default=None)
    parser.add_argument("--scenario_end", type=int, default=None)
    parser.add_argument("--topdown", action="store_true")
    args = parser.parse_args()

    env_config = {"use_render": True if not args.topdown else False}
    if args.manual_control:
        env_config["manual_control"] = True
    else:
        env_config["manual_control"] = False
        env_config["agent_policy"] = IDMPolicy

    env_class, config = create_env_and_config("env_num_3000_start_seed_0_synthetic",
                                              extra_env_config=env_config,
                                              scenario_start=args.scenario_start,
                                              scenario_end=args.scenario_end,
                                              random_set_seed_when_reset=True)
    env = env_class(config)
    try:
        while True:
            env.reset()
            for t in range(3000):
                text_to_render = {"seed": env.current_seed,
                                  "env_step (<3000)": env.engine.episode_step,
                                  "maunual_control (w,a,s,d)": args.manual_control,
                                  "reset": "press R"}
                o, r, d, i = env.step([0, 1])
                env.render(text=text_to_render,
                           **dict(mode="top_down", film_size=(800, 800)))
                if d:
                    break
    finally:
        env.close()

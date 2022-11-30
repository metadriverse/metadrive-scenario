from metadrive_scenario.utils.env_create_utils import create_env_and_config
from metadrive.policy.idm_policy import IDMPolicy, WaymoIDMPolicy
from metadrive.policy.replay_policy import ReplayEgoCarPolicy

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--manual_control", action="store_true")
    parser.add_argument("--scenario_start", type=int, required=True)
    parser.add_argument("--scenario_end", type=int, required=True)
    parser.add_argument("--topdown", action="store_true")
    parser.add_argument("--dataset", required=True, type=str)
    parser.add_argument("--idm_traffic", action="store_true")
    args = parser.parse_args()
    is_waymo = "waymo" in args.dataset

    env_config = {"use_render": True if not args.topdown else False}
    if args.manual_control:
        env_config["manual_control"] = True
    else:
        env_config["manual_control"] = False
        if is_waymo:
            if args.idm_traffic:
                env_config["agent_policy"] = WaymoIDMPolicy
            else:
                env_config["agent_policy"] = ReplayEgoCarPolicy
        else:
            env_config["agent_policy"] = IDMPolicy

    if args.idm_traffic and is_waymo:
        env_config["replay"] = False

    env_class, config = create_env_and_config(
        args.dataset,
        extra_env_config=env_config,
        scenario_start=args.scenario_start,
        scenario_end=args.scenario_end,
        random_set_seed_when_reset=True,
        waymo_env=True if is_waymo else False
    )
    env = env_class(config)
    while True:
        env.reset()
        for t in range(3000):
            text_to_render = {
                "env index": env.current_seed,
                "env_step (<3000)": env.engine.episode_step,
                "maunual_control (w,a,s,d)": args.manual_control,
                "reset": "press R"
            }
            o, r, d, i = env.step([0, 1])
            env.render(text=text_to_render, **dict(mode="top_down", film_size=(800, 800)) if args.topdown else {})
            if d:
                break

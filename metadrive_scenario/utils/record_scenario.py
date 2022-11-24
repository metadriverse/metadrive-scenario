import os

from metadrive_scenario.utils.env_create_utils import create_env_and_config
import tqdm
import pygame
from metadrive.policy.replay_policy import ReplayEgoCarPolicy

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--manual_control", action="store_true")
    parser.add_argument("--scenario_start", type=int, required=False, default=1)
    parser.add_argument("--scenario_end", type=int, required=False, default=1)
    parser.add_argument("--topdown", action="store_true")
    parser.add_argument("--dataset", required=False, type=str, default="1")
    parser.add_argument("--idm_traffic", action="store_true")
    args = parser.parse_args()
    is_waymo = True

    args.topdown = True
    args.manual_control = False
    args.dataset = "1000_waymo_training"
    args.scenario_start = 0
    args.scenario_end = 1000

    env_config = {"use_render": True if not args.topdown else False}
    if args.manual_control:
        env_config["manual_control"] = True
    else:
        env_config["manual_control"] = False
        env_config["agent_policy"] = ReplayEgoCarPolicy

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
    for seed in [4, 5, 6, 8, 14, 21, 30, 31, 33, 34, 56, 66, 72, 81, 101, 141, 143, 159, 161, 171, 213, 228, 251, 276,
                 315, 406, 446, 453, 465, 470, 492, 505, 535, 551, 562, 584, 612, 633, 634, 658, 716, 825, 870, 871,
                 888, 954, 998, ]:
        os.makedirs("{}".format(seed))
        env.reset(seed=seed)
        for step in range(1000):
            o, r, d, i = env.step([0, 1])
            ret = env.render(**dict(mode="top_down", film_size=(800, 800)) if args.topdown else {})
            pygame.image.save(ret, "{}/{}.png".format(seed, step))
            if env._env.episode_step >= len(env._env.vehicle.navigation.reference_trajectory.segment_property):
                break

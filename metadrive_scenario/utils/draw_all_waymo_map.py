from metadrive_scenario.utils.env_create_utils import create_env_and_config
import tqdm
import pygame
from metadrive.policy.idm_policy import IDMPolicy

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
    args.dataset = "env_num_1165_waymo"
    args.scenario_start = 0
    args.scenario_end = 1165

    env_config = {"use_render": True if not args.topdown else False}
    if args.manual_control:
        env_config["manual_control"] = True
    else:
        env_config["manual_control"] = False
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
    for seed in tqdm.tqdm(range(1165)):
        env.reset(seed=seed)
        o, r, d, i = env.step([0, 1])
        ret = env.render(**dict(mode="top_down", film_size=(800, 800)) if args.topdown else {})
        pygame.image.save(ret, "image/{}.png".format(seed))

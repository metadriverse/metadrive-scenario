import argparse
import os

import cv2
import pygame
import seaborn as sns
import tqdm
from metadrive.policy.replay_policy import ReplayEgoCarPolicy
from metadrive_scenario.utils.env_create_utils import create_env_and_config


def image_to_video(seed):
    image_folder = '{}'.format(seed)
    video_name = '{}.mp4'.format(seed)

    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    images.sort(key=lambda x: int(x[:-4]))
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 30, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()


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
    color = sns.color_palette("colorblind")[2]
    env = env_class(config)
    after_selection = [6, 72, 81, 159, 171, 228, 276, 446, 492, 551, 562, 584, 658, 716, 825, 954]
    before_select = [
        4,
        5,
        6,
        8,
        14,
        21,
        30,
        31,
        33,
        34,
        56,
        66,
        72,
        81,
        101,
        141,
        143,
        159,
        161,
        171,
        213,
        228,
        251,
        276,
        315,
        406,
        446,
        453,
        465,
        470,
        492,
        505,
        535,
        551,
        562,
        584,
        612,
        633,
        634,
        658,
        716,
        825,
        870,
        871,
        888,
        954,
        998,
    ]
    for seed in tqdm.tqdm(after_selection):
        os.makedirs("{}".format(seed))
        env.reset(seed=seed)
        env._env.vehicle._panda_color = color

        for step in range(1000):
            o, r, d, i = env.step([0, 1])
            ret = env.render(
                **dict(mode="top_down", film_size=(3000, 3000), screen_size=(1920,
                                                                             1080), track_target_vehicle=True) if args.
                topdown else {}
            )
            pygame.image.save(ret, "{}/{}.png".format(seed, step))
            if env._env.episode_step >= len(env._env.vehicle.navigation.reference_trajectory.segment_property):
                break
        image_to_video(seed)

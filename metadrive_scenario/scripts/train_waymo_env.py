from metadrive.envs.real_data_envs.waymo_env import WaymoEnv
from ray import tune

from metadrive_scenario.utils.training_utils import train, get_train_parser, MultiAgentDrivingCallbacks

if __name__ == '__main__':
    args = get_train_parser().parse_args()

    exp_name = args.exp_name or "TEST"
    stop = int(200_0000)

    config = dict(
        env=    register_env(env_name, lambda config: MA(config))
,
        env_config=dict(
            case_num=tune.grid_search([1, 5, 10, 20, 50]),
            waymo_data_directory="/home/qyli/waymo/all"
        ),

        # ===== Evaluation =====
        evaluation_interval=5,
        evaluation_num_episodes=20,
        evaluation_config=dict(env_config=dict(case_num=160, waymo_data_directory="/home/qyli/waymo/validation")),
        evaluation_num_workers=2,
        metrics_smoothing_episodes=50,

        # ===== Training =====
        framework="torch",
        prioritized_replay=False,
        horizon=1000,
        target_network_update_freq=1,
        timesteps_per_iteration=1000,
        learning_starts=10000,
        clip_actions=False,
        normalize_actions=True,
        num_cpus_for_driver=0.25,
        # No extra worker used for learning. But this config impact the evaluation workers.
        num_cpus_per_worker=0.25,
        # num_gpus_per_worker=0.1 if args.num_gpus != 0 else 0,
        num_gpus=0.1 if args.num_gpus != 0 else 0,
    )

    train(
        "SAC",
        exp_name=exp_name,
        keep_checkpoints_num=5,
        stop=stop,
        config=config,
        num_gpus=args.num_gpus,
        # num_seeds=args.num_seeds,
        num_seeds=5,
        test_mode=args.test,
        # local_mode=True
        wandb_key_file="~/wandb_api_key_file.txt",
        wandb_project="waymo_generalization",
        custom_callback=MultiAgentDrivingCallbacks
    )

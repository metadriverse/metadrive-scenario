from metadrive_scenario.utils.env_create_utils import create_env_and_config
from metadrive.policy.idm_policy import IDMPolicy
from metadrive.policy.replay_policy import ReplayEgoCarPolicy

if __name__ == "__main__":
    env_class, config = create_env_and_config(
        "new_1165",
        extra_env_config={
            "use_render": False,
            "manual_control": False,
            "replay": True,
            "agent_policy" : ReplayEgoCarPolicy,
        },
        random_set_seed_when_reset=False,
        scenario_start=1112,
        waymo_env=True,
        scenario_end=1113
    )
    env = env_class(config)
    for i in range(10000):
        env.reset()
        for t in range(1000):
            o, r, d, i = env.step([0, 1])
            env.render(text={"seed": env.current_seed}, mode="topdown")
            if d:
                break

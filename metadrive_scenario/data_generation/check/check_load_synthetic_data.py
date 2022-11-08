from metadrive_scenario.utils.env_create_utils import create_env
import pickle
from tqdm import tqdm
from metadrive.component.pgblock.first_block import FirstPGBlock


def check_load_synthetic_data(dataset=None):
    raise DeprecationWarning
    assert dataset, "Please assign dataset name"
    env = create_env(dataset)
    error_seed = []

    block_stat = {}
    vehicle_num = 0
    total_block_num = 0
    for seed in tqdm(range(env.config["start_seed"], env.config["start_seed"] + env.config["environment_num"]),
                     desc="Check Scenario"):
        try:
            env.reset(force_seed=seed)

            # Block Stat
            blocks_id = [b.ID for b in env.current_map.blocks]
            blocks_id.remove(FirstPGBlock.ID)
            total_block_num += len(blocks_id)
            for b_id in blocks_id:
                if b_id in block_stat:
                    block_stat[b_id] += 1
                else:
                    block_stat[b_id] = 1

            # Vehicle Stat
            vehicle_num += env.engine.traffic_manager.get_vehicle_num()

            for i in range(10):
                env.step(env.action_space.sample())
        except:
            print("Scenario error, seed: {}".format(seed))
            error_seed.append(seed)
    print("Error seeds: {}".format(error_seed))

    for k, v in block_stat.items():
        block_stat[k] = v / total_block_num

    stat_to_store = {"Average Traffic Vehicle: ": vehicle_num / env.config["environment_num"],
                     "Block Stat: ": block_stat}
    for k, v in stat_to_store.items():
        print(k, v)
    with open("stat_for_{}.pkl".format(dataset), "wb+") as file:
        pickle.dump(stat_to_store, file)


if __name__ == "__main__":
    raise DeprecationWarning
    dataset = "synthetic_env_num_3000_start_seed_0"
    check_load_synthetic_data(dataset)

import os
import shutil

from metadrive_scenario import METADRIVE_SCENARIO_DATASET_DIR
from tqdm import tqdm
from metadrive.utils.waymo_utils.waymo_utils import CustomUnpickler


def get_original_case_id(directory_path, start_idx, end_idx):
    ret = []
    for i in tqdm(range(start_idx, end_idx), desc="Check Waymo Data"):
        file_path = os.path.join(directory, "{}.pkl".format(i))
        assert os.path.exists(file_path), "No Data {}".format(i)
        data = CustomUnpickler(open(file_path, "rb+")).load()
        ret.append(data["id"])
    return ret


def get_file_from_original_ids(directory_path, ids: list):
    ret = []

    def isfile(path):
        return True if ".pkl" in path else False

    for file_path in tqdm([os.path.join(directory_path, f) for f in os.listdir(directory_path) if
                           isfile(os.path.join(directory_path, f))],
                          desc="Check Waymo Data"):
        data = CustomUnpickler(open(file_path, "rb+")).load()
        if data["id"] in ids:
            ret.append(file_path)
    print("Get {} files from {} ids".format(len(ret), len(ids)))
    return ret


def copy_case(case_pathes: list, destination_dir):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    for idx, case_original_path in tqdm(enumerate(case_pathes)):
        file_dest_path = os.path.join(destination_dir, str(idx)) + ".pkl"
        shutil.copyfile(case_original_path, file_dest_path)


def get_same_cases_id(directory, start_idx, end_idx):
    "There are same case id in the original Waymo data. Use this function to retrieve them"
    ret = {}
    for i in tqdm(range(start_idx, end_idx), desc="Check Waymo Data"):
        file_path = os.path.join(directory, "{}.pkl".format(i))
        assert os.path.exists(file_path), "No Data {}".format(i)
        data = CustomUnpickler(open(file_path, "rb+")).load()
        if data["id"] in ret:
            ret[data["id"]].append(i)
        else:
            ret[data["id"]] = [i]
    return ret


if __name__ == "__main__":
    # for k, v in get_same_cases_id(os.path.join(METADRIVE_SCENARIO_DATASET_DIR, "new_1165"), 0, 1187).items():
    #     if len(v) > 1:
    #         print(k, v)

    # For rebuilding dataset
    directory = os.path.join(METADRIVE_SCENARIO_DATASET_DIR, "env_num_1165_waymo")
    dest_dir = "D:\\code\\waymo_20s\\training_20s_processed"
    ids = get_original_case_id(directory, 0, 1165)
    files = get_file_from_original_ids(dest_dir, ids)
    copy_case(files, os.path.join(METADRIVE_SCENARIO_DATASET_DIR, "new_1165"))

    # '6b1c1b106c54e11d'
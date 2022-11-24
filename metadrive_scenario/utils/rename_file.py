import os

from tqdm import tqdm


def unify_name(inut_path, offset=1000):
    file_list = os.listdir(inut_path)
    file_list.sort()
    for k, file_name in enumerate(tqdm(file_list)):
        file_path = os.path.join(inut_path, file_name)
        new_file_path = os.path.join(inut_path, "{}.pkl".format(offset + k))
        os.rename(file_path, new_file_path)


if __name__ == "__main__":
    raise ValueError("Be cautious when running this sceipt!")
    import sys

    raw_data_path = "../dataset/env_num_1175_waymo"
    # raw_data_path = ".\\debug_data"
    unify_name(raw_data_path, offset=0)

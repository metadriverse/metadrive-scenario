import os

METADRIVE_SCENARIO_ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
METADRIVE_SCENARIO_DATASET_DIR = os.path.join(METADRIVE_SCENARIO_ROOT_DIR, "dataset")


class DataType:
    SYNTHETIC = "synthetic"

from metadrive.component.algorithm.blocks_prob_dist import PGBlockDistConfig
from metadrive.component.pgblock.bidirection import Bidirection
from metadrive.component.pgblock.bottleneck import Merge, Split
from metadrive.component.pgblock.curve import Curve
from metadrive.component.pgblock.fork import InFork, OutFork
from metadrive.component.pgblock.parking_lot import ParkingLot
from metadrive.component.pgblock.ramp import InRampOnStraight, OutRampOnStraight
from metadrive.component.pgblock.roundabout import Roundabout
from metadrive.component.pgblock.intersection import InterSection
from metadrive.component.pgblock.t_intersection import TInterSection
from metadrive.component.pgblock.straight import Straight
from metadrive.component.pgblock.tollgate import TollGate


class DatasetPGBlockConfig(PGBlockDistConfig):
    MAX_LANE_NUM = 4
    MIN_LANE_NUM = 1

    BLOCK_TYPE_DISTRIBUTION_V1 = None  # set to null
    BLOCK_TYPE_DISTRIBUTION_V2 = None  # set to null

    BLOCK_TYPE_DISTRIBUTION_DATASET = {
        # 0.3 for curves
        Curve: 0.2,
        # 0.3 for straight
        Straight: 0.1,
        InRampOnStraight: 0.1,
        OutRampOnStraight: 0.1,
        # 0.3 for intersection
        InterSection: 0.1,
        TInterSection: 0.1,
        # 0.1 for roundabout
        Roundabout: 0.1,
        InFork: 0.00,
        OutFork: 0.00,
        Merge: 0.1,
        Split: 0.1,
        ParkingLot: 0.00,
        TollGate: 0.00,
        Bidirection: 0.00
    }

    @classmethod
    def all_blocks(cls, version: str = "v2"):
        return list(cls._get_dist(version).keys())

    @classmethod
    def get_block(cls, block_id: str, version: str = "v2"):
        for block in cls.all_blocks(version):
            if block.ID == block_id:
                return block
        raise ValueError("No {} block type".format(block_id))

    @classmethod
    def block_probability(cls, version: str = "v2"):
        return list(cls._get_dist(version).values())

    @classmethod
    def _get_dist(cls, version: str):
        return cls.BLOCK_TYPE_DISTRIBUTION_DATASET

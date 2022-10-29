from metadrive.component.algorithm.blocks_prob_dist import PGBlockConfig
from metadrive.component.pgblock.bottleneck import Merge, Split
from metadrive.component.pgblock.curve import Curve
from metadrive.component.pgblock.fork import InFork, OutFork
from metadrive.component.pgblock.parking_lot import ParkingLot
from metadrive.component.pgblock.ramp import InRampOnStraight, OutRampOnStraight
from metadrive.component.pgblock.roundabout import Roundabout
from metadrive.component.pgblock.std_intersection import StdInterSection
from metadrive.component.pgblock.std_t_intersection import StdTInterSection
from metadrive.component.pgblock.straight import Straight
from metadrive.component.pgblock.tollgate import TollGate
from metadrive.component.pgblock.bidirection import Bidirection


class DatasetPGBlockConfig(PGBlockConfig):
    BLOCK_TYPE_DISTRIBUTION_V1 = None  # set to null
    BLOCK_TYPE_DISTRIBUTION_V2 = None  # set to null

    BLOCK_TYPE_DISTRIBUTION_V3 = {
        # 0.3 for curves
        Curve: 0.1,
        # 0.3 for straight
        Straight: 0.1,
        InRampOnStraight: 0.1,
        OutRampOnStraight: 0.1,
        # 0.3 for intersection
        StdInterSection: 0.1,
        StdTInterSection: 0.1,
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

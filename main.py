import random

from app.internal.level import LevelFactory
from app.internal.magic_lamp import MagicLampService, UsualMagicLamp
import numpy as np


if __name__ == '__main__':
    lvl_factory = LevelFactory()
    level = lvl_factory.create(level_value=74, percent_collected=99.69)
    need_for_up = level.get_experience_for_next_level()

    service = MagicLampService()
    lamps_count = 2
    lamps = [UsualMagicLamp() for _ in range(lamps_count)]
    experiences_from_lamps = np.array([
        service.calculate_average_experience(lamps)
        for _ in range(30000)
    ])
    # experience_from_lamps = experiences_from_lamps / 10000
    experience_from_lamps = np.percentile(experiences_from_lamps, 90)

    print('For level:', need_for_up)
    print('Lamps its:', experience_from_lamps)
    print('Level is upped:', need_for_up < experience_from_lamps)

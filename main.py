from typing import Iterable

from app.internal.level import LevelFactory
from app.internal.magic_lamp import ExtendedMagicLamp
from app.internal.random_variable import DiscreteRandomVariablesSumma
from app.internal.random_variable import DRV
from app.internal.random_variable import DCDF
import numpy as np


def get_upgrade_probablity(rv_generator: Iterable[DRV[int]], value: int) -> Iterable[float]:
    rv_summa = DiscreteRandomVariablesSumma()
    current_rv = None

    for index, rv in enumerate(rv_generator):
        if index == 0:
            current_rv = rv
        else:
            current_rv = rv_summa.calculate(current_rv, rv)

        yield 1 - DCDF(current_rv).left_limit_at(value)


if __name__ == '__main__':
    lvl_factory = LevelFactory()
    level = lvl_factory.create(level_value=76, percent_collected=1.00)
    need_for_up = level.get_experience_for_next_level()

    max_lamps_count = 60
    lamps = [ExtendedMagicLamp() for _ in range(max_lamps_count)]
    

    print('For level:', need_for_up)

    probabilities_generator = get_upgrade_probablity(lamps, need_for_up)
    for index, probability in enumerate(probabilities_generator):
        print('Lamps count:', index + 1)
        print('Upgrade probability:', probability)

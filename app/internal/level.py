from abc import ABCMeta, abstractmethod


class AbstractLevel(metaclass=ABCMeta):
    @abstractmethod
    def get_experience_for_next_level(self) -> int:
        raise NotImplementedError()


class Level(AbstractLevel):
    NEED_FOR_UP = {
        73: 1523534179,
        74: 1919653065,
        75: 2437959394,
        76: 3120588023,
        77: 4056764430,
        78: 5476631981,
    }

    def __init__(self, level_value: int, percent_collected: float):
        self._level_value = level_value
        self._percent_collected = percent_collected

    def get_experience_for_next_level(self) -> int:
        if self._level_value not in self.NEED_FOR_UP:
            raise ValueError(f'Not found level {self._level_value}')

        if self._level_value + 1 not in self.NEED_FOR_UP:
            raise ValueError(f'Not found level {self._level_value + 1}')

        need_for_next_level = self.NEED_FOR_UP[self._level_value + 1]
        experience_filled = (self._percent_collected / 100) * need_for_next_level

        return need_for_next_level - int(experience_filled)


class AbstractLevelFactory(metaclass=ABCMeta):
    @abstractmethod
    def create(self, level_value: int, percent_collected: float) -> AbstractLevel:
        raise NotImplementedError()


class LevelFactory(AbstractLevelFactory):
    def create(self, level_value: int, percent_collected: float) -> AbstractLevel:
        return Level(level_value, percent_collected)

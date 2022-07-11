from abc import ABCMeta
from abc import abstractmethod
from collections import defaultdict
from typing import Any
from typing import Generic
from typing import Mapping
from typing import TypeVar


class Comparable(metaclass=ABCMeta):
    @abstractmethod
    def __lt__(self, other: Any) -> bool: ...


T = TypeVar('T', bound=Comparable)


class RandomVariableError(Exception):
    pass


class UnknownValueError(Generic[T], RandomVariableError):
    def __init__(self, value: T) -> None:
        self.value = value

        super().__init__(f'Unkown value: {self.value}')


class RandomVariable(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def get_probability(value: T) -> float:
        raise NotImplementedError()


RV = RandomVariable


class DiscreteRandomVariable(RandomVariable[T], metaclass=ABCMeta):
    @property
    @abstractmethod
    def probabilities(self) -> Mapping[T, float]:
        raise NotImplementedError()

    def get_probability(self, value: T) -> float:
        try:
            return self.probabilities[value]
        except KeyError:
            raise UnknownValueError(value)


DRV = DiscreteRandomVariable
TRandomVariable = TypeVar('TRandomVariable', bound=RandomVariable)


class AbstractCumulativeDistributionFunction(Generic[TRandomVariable], metaclass=ABCMeta):
    def __init__(self, random_variable: TRandomVariable) -> None:
        self._random_variable = random_variable

    @abstractmethod
    def value_at(value: T) -> float:
        raise NotImplementedError()

    @abstractmethod
    def left_limit_at(value: T) -> float:
        raise NotImplementedError()


CDF = AbstractCumulativeDistributionFunction


class DiscreteCumulativeDistributionFunction(CDF[DRV[T]]):
    def value_at(self, value: T) -> float:
        probabilities = self._random_variable.probabilities
        return sum(probabilities[v] for v in probabilities if v <= value)

    def left_limit_at(self, value: T) -> float:
        probabilities = self._random_variable.probabilities
        return sum(probabilities[v] for v in probabilities if v < value)


DCDF = DiscreteCumulativeDistributionFunction


class AbstractRandomVariablesOperation(Generic[TRandomVariable], metaclass=ABCMeta):
    @abstractmethod
    def calculate(
        self,
        first_random_variable: TRandomVariable,
        second_random_variable: TRandomVariable,
    ) -> TRandomVariable:
        raise NotImplementedError()


Operation = AbstractRandomVariablesOperation


class DiscreteRandomVariablesSumma(Operation[DRV[T]]):
    def calculate(
        self,
        first_random_variable: DRV[T],
        second_random_variable: DRV[T],
    ) -> DRV:
        probabilities: Mapping[T, float] = defaultdict(float)

        for first_value in first_random_variable.probabilities:
            for second_value in second_random_variable.probabilities:
                probabilities[first_value + second_value] += (
                    first_random_variable.get_probability(first_value) *
                    second_random_variable.get_probability(second_value)
                )

        class _DRV(DRV[T]):
            @property
            def probabilities(self) -> Mapping[T, float]:
                return probabilities

        return _DRV()

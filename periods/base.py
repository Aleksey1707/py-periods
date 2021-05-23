from abc import ABC, abstractmethod
from typing import TypeVar, Any, Union

PERIOD_TYPE = TypeVar('PERIOD_TYPE')
ITEM_TYPE = Union[PERIOD_TYPE, 'Period']


class Period(ABC):
    begin: PERIOD_TYPE
    end: PERIOD_TYPE

    data: Any
    protect_data: bool

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __contains__(self, item: ITEM_TYPE):
        pass

    @abstractmethod
    def __lt__(self, other: ITEM_TYPE):
        pass

    @abstractmethod
    def __le__(self, other: ITEM_TYPE):
        pass

    @abstractmethod
    def __eq__(self, other: ITEM_TYPE):
        pass

    @abstractmethod
    def __ne__(self, other: ITEM_TYPE):
        pass

    @abstractmethod
    def __gt__(self, other: ITEM_TYPE):
        pass

    @abstractmethod
    def __ge__(self, other: ITEM_TYPE):
        pass

    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __add__(self, other: ITEM_TYPE):
        pass

    @abstractmethod
    def __sub__(self, other: ITEM_TYPE):
        pass

    @abstractmethod
    def __hash__(self):
        pass

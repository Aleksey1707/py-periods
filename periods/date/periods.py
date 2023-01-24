import copy
import datetime
from typing import Union, Any, List, Optional

from periods.base import Period

PERIOD_TYPE = Union[datetime.date, datetime.datetime]
CLASS_ITEM_TYPE = 'DatePeriod'
FULL_ITEM_TYPE = Union[PERIOD_TYPE, CLASS_ITEM_TYPE]


class DatePeriod(Period):
    """
    Класс для работы с периодами дат
    """

    protect_data = False

    __delta = datetime.timedelta(days=1)

    def __init__(self, begin: PERIOD_TYPE, end: PERIOD_TYPE,
                 data: Any = None, protect_data: bool = False):

        self._check_periods(begin, end)

        self.begin = self._normalize_period(begin)
        self.end = self._normalize_period(end)

        self.data = data
        self.protect_data = protect_data

    @staticmethod
    def _normalize_period(period: PERIOD_TYPE):
        if isinstance(period, datetime.datetime):
            return period.date()

        return period

    @staticmethod
    def _check_periods(begin: PERIOD_TYPE, end: PERIOD_TYPE):
        if not isinstance(begin, (datetime.date, datetime.datetime)):
            raise TypeError

        if begin > end:
            raise ValueError('Wrong dates')

    def __hash__(self):
        return hash((self.begin, self.end))

    def __str__(self) -> str:
        return '{} - {}'.format(self.begin.strftime('%d.%m.%Y'), self.end.strftime('%d.%m.%Y'))

    def __iter__(self) -> PERIOD_TYPE:
        for x in [self.begin + datetime.timedelta(days=d) for d in
                  range((self.end - self.begin).days + 1)]:
            yield x

    def __contains__(self, item: FULL_ITEM_TYPE) -> bool:
        """Проверка вхождения даты/периода в данный период"""
        if isinstance(item, type(self.begin)):
            return self.begin <= item <= self.end
        elif isinstance(item, DatePeriod):
            return self.begin <= item.begin <= self.end and \
                   self.begin <= item.end <= self.end
        else:
            raise TypeError

    def __lt__(self, other: FULL_ITEM_TYPE) -> bool:
        """Проверка того, что данный период закончился раньше сравниваемой даты/периода и они НЕ ПЕРЕСЕКАЮТСЯ"""
        if isinstance(other, type(self.begin)):
            return self.end < other
        elif isinstance(other, DatePeriod):
            if self.__contains__(other) or self.is_crossing(other):
                return False

            return self.end < other.begin
        else:
            raise TypeError

    def __le__(self, other: CLASS_ITEM_TYPE) -> bool:
        """Проверка того, что данный период закончился раньше переданной периода и они ПЕРЕСЕКАЮТСЯ"""
        if not isinstance(other, DatePeriod):
            raise TypeError

        if not self.is_crossing(other):
            return False

        if (self == other) or (self in other) or (other in self):
            return False

        return self.end <= other.end

    def __eq__(self, other: FULL_ITEM_TYPE) -> bool:
        """Проверка того, что данный период идентичен второму периоду"""
        if isinstance(other, type(self.begin)):
            return False
        elif isinstance(other, DatePeriod):
            return self.begin == other.begin and self.end == other.end
        else:
            raise TypeError

    def __ne__(self, other: FULL_ITEM_TYPE) -> bool:
        """Проверка того, что данный период не является идентчиным второму периоду"""
        if isinstance(other, type(self.begin)):
            return True
        elif isinstance(other, DatePeriod):
            return self.begin != other.begin or self.end != other.end
        else:
            raise TypeError

    def __gt__(self, other: FULL_ITEM_TYPE) -> bool:
        """Проверка того, что данный период закончился позже сравниваемой даты/периода и они НЕ ПЕРЕСЕКАЮТСЯ"""
        if isinstance(other, type(self.begin)):
            return other < self.begin
        elif isinstance(other, DatePeriod):
            if self in other or self.is_crossing(other):
                return False

            return other.end < self.begin
        else:
            raise TypeError

    def __ge__(self, other: CLASS_ITEM_TYPE) -> bool:
        """Проверка того, что данный период закончился позже переданной периода и они ПЕРЕСЕКАЮТСЯ"""
        if not isinstance(other, DatePeriod):
            raise TypeError

        if not self.is_crossing(other):
            return False

        if (other in self) or (self in other):
            return False

        return self.end > other.end

    def __len__(self):
        """Количество дней в периоде"""
        return (self.end - self.begin).days + 1

    def __add__(self, other: CLASS_ITEM_TYPE) -> List[CLASS_ITEM_TYPE]:
        """Производит операцию добавления периода"""
        if not isinstance(other, DatePeriod):
            raise TypeError

        if self not in other and not self.is_crossing(other):
            return [self, other]

        if other in self:
            return [
                self,
            ]
        elif self in other:
            if self.protect_data:
                other_copy = copy.copy(other)
                other_copy.data = self.data
                return [
                    other_copy,
                ]
            else:
                return [
                    other,
                ]
        elif self <= other:
            return [
                DatePeriod(self.begin, other.end, self.data),
            ]
        elif self >= other:
            return [
                DatePeriod(other.begin, self.end, self.data),
            ]
        else:
            raise ValueError

    def __sub__(self, other: CLASS_ITEM_TYPE) -> List[CLASS_ITEM_TYPE]:
        """Производит операцию вычитания периода"""
        if not isinstance(other, DatePeriod):
            raise TypeError

        if self not in other and not self.is_crossing(other):
            return [self, ]

        cross = self.crossing(other)

        if (self == other) or (self in other):
            return []
        elif other in self:
            if self.begin == other.begin:
                return [
                    DatePeriod(cross.end + self.__delta, self.end, self.data)
                ]
            elif self.end == other.end:
                return [
                    DatePeriod(self.begin, cross.begin - self.__delta, self.data)
                ]
            else:
                return [
                    DatePeriod(self.begin, cross.begin - self.__delta, self.data),
                    DatePeriod(cross.end + self.__delta, self.end, self.data)
                ]
        elif self <= other:
            return [
                DatePeriod(self.begin, cross.begin - self.__delta, self.data),
            ]
        elif self >= other:
            return [
                DatePeriod(cross.end + self.__delta, self.end, self.data)
            ]
        else:
            raise ValueError

    def split(self, other: CLASS_ITEM_TYPE) -> List[CLASS_ITEM_TYPE]:
        """Разбиение данного периода на периоды по переданному периоду (other)"""
        if not isinstance(other, DatePeriod):
            raise TypeError

        if self not in other and not self.is_crossing(other):
            return [self, ]

        if self == other:
            return [self, ]

        cross = self.crossing(other)

        if self <= other:
            return [
                DatePeriod(self.begin, cross.begin - self.__delta, self.data),
                cross,
                DatePeriod(cross.end + self.__delta, other.end, self.data)
            ]
        elif self >= other:
            return [
                DatePeriod(other.begin, cross.begin - self.__delta, self.data),
                cross,
                DatePeriod(cross.end + self.__delta, self.end, self.data)
            ]
        elif other in self:
            if self.begin == other.begin:
                return [
                    DatePeriod(other.begin, other.end, self.data),
                    DatePeriod(other.end + self.__delta, self.end, self.data)
                ]
            elif self.end == other.end:
                return [
                    DatePeriod(self.begin, other.begin - self.__delta, self.data),
                    DatePeriod(other.begin, other.end, self.data)
                ]
            else:
                return [
                    DatePeriod(self.begin, cross.begin - self.__delta, self.data),
                    cross,
                    DatePeriod(cross.end + self.__delta, self.end, self.data)
                ]
        elif self in other:
            return [self, ]
        else:
            raise ValueError

    def is_crossing(self, period: CLASS_ITEM_TYPE) -> bool:
        """Проверка того, что текущий период (self) пересекается с переданным периодом (other)."""
        if not isinstance(period, DatePeriod):
            raise TypeError

        return self.begin <= period.begin <= self.end or \
               self.begin <= period.end <= self.end or \
               period.begin <= self.begin <= period.end or \
               period.begin <= self.end <= period.end

    def crossing(self, other: CLASS_ITEM_TYPE) -> Optional[CLASS_ITEM_TYPE]:
        """Получение пересечения текущего периода (self) с переданным периодом (other)."""
        if not isinstance(other, DatePeriod):
            raise TypeError

        if self.is_crossing(other):
            begin_date = max(self.begin, other.begin)
            end_date = min(self.end, other.end)
            return DatePeriod(begin_date, end_date, self.data)

        return

    def must_crossing(self, other: CLASS_ITEM_TYPE) -> Optional[CLASS_ITEM_TYPE]:
        """Получение пересечения текущего периода (self) с переданным периодом (other)."""
        if not isinstance(other, DatePeriod):
            raise TypeError

        result = self.crossing(other)
        if result is None:
            raise ValueError

        return result

    @classmethod
    def circle_sub(cls, period1: List[CLASS_ITEM_TYPE], period2: List[CLASS_ITEM_TYPE]) -> List[CLASS_ITEM_TYPE]:
        """Циклическое вычетание периодов"""
        res = []

        if not period1:
            return res

        if not period2:
            return period1

        for p1 in period1:
            out = False
            for p2 in period2:
                if p1.is_crossing(p2):
                    res.extend(p1 - p2)
                    res = cls.circle_sub(res, period2)
                    out = True
                    break
            else:
                if not out:
                    res.append(p1)
        return res

    @classmethod
    def circle_crossing(cls, period1: List[CLASS_ITEM_TYPE], period2: List[CLASS_ITEM_TYPE]) -> List[CLASS_ITEM_TYPE]:
        """Циклическое пересечение периодов"""

        res = []

        if not period1:
            return res

        if not period2:
            return period1

        for p1 in period1:
            for p2 in period2:
                if p1.is_crossing(p2):
                    res.extend([p1.crossing(p2)])
        return res

    @classmethod
    def circle_add(cls, period1: List[CLASS_ITEM_TYPE], period2: List[CLASS_ITEM_TYPE]) -> List[CLASS_ITEM_TYPE]:
        """Циклическое сложение периодов"""
        res = []

        if not period1:
            return res

        if not period2:
            return period1

        for p1 in period1:
            for p2 in period2:
                res.extend(p1 + p2)
        return res

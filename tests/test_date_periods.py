# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import copy
import datetime

import unittest

from periods.date.periods import DatePeriod


class DatePeriodTest(unittest.TestCase):
    """
    Тестирование DatePeriod

    1) Не пересекающиеся периоды
        p11 (DatePeriod): |========|
        p12 (DatePeriod):             |=========|

    2) Пересекающиеся периоды, пересечение в несколько дней
        p21 (DatePeriod): |========|
        p22 (DatePeriod):      |=========|

    3) Пересекающиеся периоды, пересечение в один день
        p31 (DatePeriod): |========|
        p32 (DatePeriod):          |=========|

    4) Вхождение периодов
        p41 (DatePeriod): |========|
        p42 (DatePeriod):   |===|

    5) Пересекающиеся периоды, пересечение в несколько дней, p51.begin = p52.begin
        p51 (DatePeriod): |========|
        p52 (DatePeriod): |===|

    6) Пересекающиеся периоды, пересечение в несколько дней, p61.end = p62.end
        p61 (DatePeriod): |========|
        p62 (DatePeriod):      |===|

    7) Пересекающиеся периоды, p71.begin = p72.begin, len(p72) = 1
        p71 (DatePeriod): |========|
        p72 (DatePeriod): |

    8) Пересекающиеся периоды, p81.end = p82.end, len(p82) = 1
        p81 (DatePeriod): |========|
        p82 (DatePeriod):          |

    9) Пересекающиеся периоды, len(p92) = 1
        p91 (DatePeriod): |========|
        p92 (DatePeriod):     |

    10) Не пересекающиеся периоды, len(pA2) = 1
        pA1 (DatePeriod):     |========|
        pA2 (DatePeriod):  |

    11) Не пересекающиеся периоды, len(pB2) = 1
        pB1 (DatePeriod):  |========|
        pB2 (DatePeriod):               |

    12) Не пересекающиеся однодневные периоды
        pC1 (DatePeriod):   |
        pC2 (DatePeriod):         |
    """

    def setUp(self) -> None:
        self.p11 = DatePeriod(datetime.date(2020, 1, 1), datetime.date(2020, 1, 25), data='p11')
        self.p12 = DatePeriod(datetime.date(2020, 2, 5), datetime.date(2020, 2, 29), data='p12')

        self.p21 = DatePeriod(datetime.date(2020, 1, 1), datetime.date(2020, 1, 31), data='p21')
        self.p22 = DatePeriod(datetime.date(2020, 1, 25), datetime.date(2020, 2, 29), data='p22')

        self.p31 = DatePeriod(datetime.date(2020, 1, 1), datetime.date(2020, 1, 31), data='p31')
        self.p32 = DatePeriod(datetime.date(2020, 1, 31), datetime.date(2020, 2, 29), data='p32')

        self.p41 = DatePeriod(datetime.date(2020, 1, 1), datetime.date(2020, 2, 29), data='p41')
        self.p42 = DatePeriod(datetime.date(2020, 1, 25), datetime.date(2020, 2, 5), data='p42')

        self.p51 = DatePeriod(datetime.date(2020, 1, 1), datetime.date(2020, 1, 31), data='p51')
        self.p52 = DatePeriod(datetime.date(2020, 1, 1), datetime.date(2020, 1, 15), data='p52')

        self.p61 = DatePeriod(datetime.date(2020, 1, 1), datetime.date(2020, 1, 31), data='p61')
        self.p62 = DatePeriod(datetime.date(2020, 1, 15), datetime.date(2020, 1, 31), data='p62')

        self.p71 = DatePeriod(datetime.date(2020, 1, 1), datetime.date(2020, 1, 31), data='p71')
        self.p72 = DatePeriod(datetime.date(2020, 1, 1), datetime.date(2020, 1, 1), data='p72')

        self.p81 = DatePeriod(datetime.date(2020, 1, 1), datetime.date(2020, 1, 31), data='p81')
        self.p82 = DatePeriod(datetime.date(2020, 1, 31), datetime.date(2020, 1, 31), data='p82')

        self.p91 = DatePeriod(datetime.date(2020, 1, 1), datetime.date(2020, 1, 31), data='p91')
        self.p92 = DatePeriod(datetime.date(2020, 1, 15), datetime.date(2020, 1, 15), data='p92')

        self.pA1 = DatePeriod(datetime.date(2020, 2, 1), datetime.date(2020, 2, 29), data='pA1')
        self.pA2 = DatePeriod(datetime.date(2020, 1, 15), datetime.date(2020, 1, 15), data='pA2')

        self.pB1 = DatePeriod(datetime.date(2020, 1, 1), datetime.date(2020, 1, 31), data='pB1')
        self.pB2 = DatePeriod(datetime.date(2020, 2, 15), datetime.date(2020, 2, 15), data='pB2')

        self.pC1 = DatePeriod(datetime.date(2020, 1, 1), datetime.date(2020, 1, 1), data='pC1')
        self.pC2 = DatePeriod(datetime.date(2020, 1, 7), datetime.date(2020, 1, 7), data='pC2')

    # -------------------------------------------Условные операторы-----------------------------------------

    def test_contains(self):
        """Тестирование __contains__ / in"""

        # ======================== Периоды ======================

        # Нет пересечения
        self.assertFalse(self.p11 in self.p12)
        self.assertFalse(self.p12 in self.p11)

        # Есть пересечение в несколько дней
        self.assertFalse(self.p21 in self.p22)
        self.assertFalse(self.p22 in self.p21)

        # Есть пересечение в один день
        self.assertFalse(self.p31 in self.p32)
        self.assertFalse(self.p32 in self.p31)

        # Периоды равны
        self.assertTrue(self.p21 in self.p21)

        # Вхождение периодов
        self.assertFalse(self.p41 in self.p42)
        self.assertTrue(self.p42 in self.p41)

        # !!!!!

        # Пересекающиеся периоды, пересечение в несколько дней, p51.begin = p52.begin
        self.assertFalse(self.p51 in self.p52)
        self.assertTrue(self.p52 in self.p51)

        # Пересекающиеся периоды, пересечение в несколько дней, p61.end = p62.end
        self.assertFalse(self.p61 in self.p62)
        self.assertTrue(self.p62 in self.p61)

        # Пересекающиеся периоды, p71.begin = p72.begin, len(p72) = 1
        self.assertFalse(self.p71 in self.p72)
        self.assertTrue(self.p72 in self.p71)

        # Пересекающиеся периоды, p81.end = p82.end, len(p82) = 1
        self.assertFalse(self.p81 in self.p82)
        self.assertTrue(self.p82 in self.p81)

        # Пересекающиеся периоды, len(p92) = 1
        self.assertFalse(self.p91 in self.p92)
        self.assertTrue(self.p92 in self.p91)

        # Не пересекающиеся периоды, len(pA2) = 1
        self.assertFalse(self.pA1 in self.pA2)
        self.assertFalse(self.pA2 in self.pA1)

        # Не пересекающиеся периоды, len(pB2) = 1
        self.assertFalse(self.pB1 in self.pB2)
        self.assertFalse(self.pB2 in self.pB1)

        # Однодневные периоды, len(pC1) = len(pC2) = 1
        self.assertFalse(self.pC1 in self.pC2)
        self.assertFalse(self.pC2 in self.pC1)

        # Однодневные периоды равны, len(pC1) = 1
        self.assertTrue(self.pC1 in self.pC1)

        # ======================== Даты ======================

        # Дата является началом периода
        self.assertTrue(self.p11.begin in self.p11)
        # Дата является началом периода + 1 день
        self.assertTrue(self.p11.begin + datetime.timedelta(days=1) in self.p11)
        # Дата является началом периода - 1 день
        self.assertFalse(self.p11.begin - datetime.timedelta(days=1) in self.p11)
        # Дата является началом периода - 10 дней
        self.assertFalse(self.p11.begin - datetime.timedelta(days=10) in self.p11)

        # Дата является концом периода
        self.assertTrue(self.p11.end in self.p11)
        # Дата является концом периода + 1 день
        self.assertFalse(self.p11.end + datetime.timedelta(days=1) in self.p11)
        # Дата является концом периода + 10 день
        self.assertFalse(self.p11.end + datetime.timedelta(days=10) in self.p11)
        # Дата является концом периода - 1 день
        self.assertTrue(self.p11.end - datetime.timedelta(days=1) in self.p11)

    def test_lt(self):
        """Тестирование __lt__ / <"""

        # ======================== Периоды ======================

        # Нет пересечения
        self.assertTrue(self.p11 < self.p12)
        self.assertFalse(self.p12 < self.p11)

        # Есть пересечение в несколько дней
        self.assertFalse(self.p21 < self.p22)
        self.assertFalse(self.p22 < self.p21)

        # Есть пересечение в один день
        self.assertFalse(self.p31 < self.p32)
        self.assertFalse(self.p32 < self.p31)

        # Периоды равны
        self.assertFalse(self.p21 < self.p21)

        # Вхождение периодов
        self.assertFalse(self.p41 < self.p42)
        self.assertFalse(self.p42 < self.p41)

        # !!!!!

        # Пересекающиеся периоды, пересечение в несколько дней, p51.begin = p52.begin
        self.assertFalse(self.p51 < self.p52)
        self.assertFalse(self.p52 < self.p51)

        # Пересекающиеся периоды, пересечение в несколько дней, p61.end = p62.end
        self.assertFalse(self.p61 < self.p62)
        self.assertFalse(self.p62 < self.p61)

        # Пересекающиеся периоды, p71.begin = p72.begin, len(p72) = 1
        self.assertFalse(self.p71 < self.p72)
        self.assertFalse(self.p72 < self.p71)

        # Пересекающиеся периоды, p81.end = p82.end, len(p82) = 1
        self.assertFalse(self.p81 < self.p82)
        self.assertFalse(self.p82 < self.p81)

        # Пересекающиеся периоды, len(p92) = 1
        self.assertFalse(self.p91 < self.p92)
        self.assertFalse(self.p92 < self.p91)

        # Не пересекающиеся периоды, len(pA2) = 1
        self.assertFalse(self.pA1 < self.pA2)
        self.assertTrue(self.pA2 < self.pA1)

        # Не пересекающиеся периоды, len(pB2) = 1
        self.assertTrue(self.pB1 < self.pB2)
        self.assertFalse(self.pB2 < self.pB1)

        # Не пересекающиеся периоды, len(pB2) = 1
        self.assertTrue(self.pB1 < self.pB2)
        self.assertFalse(self.pB2 < self.pB1)

        # Однодневные периоды, len(pC1) = len(pC2) = 1
        self.assertTrue(self.pC1 < self.pC2)
        self.assertFalse(self.pC2 < self.pC1)

        # Однодневные периоды равны, len(pC1) = 1
        self.assertFalse(self.pC1 < self.pC1)

        # ======================== Даты ======================

        # Дата является началом периода
        self.assertFalse(self.p11 < self.p11.begin)
        # Дата является началом периода + 1 день
        self.assertFalse(self.p11 < self.p11.begin + datetime.timedelta(days=1))
        # Дата является началом периода - 1 день
        self.assertFalse(self.p11 < self.p11.begin - datetime.timedelta(days=1))
        # Дата является началом периода - 10 дней
        self.assertFalse(self.p11 < self.p11.begin - datetime.timedelta(days=10))

        # Дата является концом периода
        self.assertFalse(self.p11 < self.p11.end)
        # Дата является концом периода + 1 день
        self.assertTrue(self.p11 < self.p11.end + datetime.timedelta(days=1))
        # Дата является концом периода + 10 день
        self.assertTrue(self.p11 < self.p11.end + datetime.timedelta(days=10))
        # Дата является концом периода - 1 день
        self.assertFalse(self.p11 < self.p11.end - datetime.timedelta(days=1))

    def test_le(self):
        """Тестирование __le__ / <="""

        # ======================== Периоды ======================

        # Нет пересечения
        self.assertFalse(self.p11 <= self.p12)
        self.assertFalse(self.p12 <= self.p11)

        # Есть пересечение в несколько дней
        self.assertTrue(self.p21 <= self.p22)
        self.assertFalse(self.p22 <= self.p21)

        # Есть пересечение в один день
        self.assertTrue(self.p31 <= self.p32)
        self.assertFalse(self.p32 <= self.p31)

        # Периоды равны
        self.assertFalse(self.p21 <= self.p21)

        # Вхождение периодов
        self.assertFalse(self.p41 <= self.p42)
        self.assertFalse(self.p42 <= self.p41)

        # !!!!!

        # Пересекающиеся периоды, пересечение в несколько дней, p51.begin = p52.begin
        self.assertFalse(self.p51 <= self.p52)
        self.assertFalse(self.p52 <= self.p51)

        # Пересекающиеся периоды, пересечение в несколько дней, p61.end = p62.end
        self.assertFalse(self.p61 <= self.p62)
        self.assertFalse(self.p62 <= self.p61)

        # Пересекающиеся периоды, p71.begin = p72.begin, len(p72) = 1
        self.assertFalse(self.p71 <= self.p72)
        self.assertFalse(self.p72 <= self.p71)

        # Пересекающиеся периоды, p81.end = p82.end, len(p82) = 1
        self.assertFalse(self.p81 <= self.p82)
        self.assertFalse(self.p82 <= self.p81)

        # Пересекающиеся периоды, len(p92) = 1
        self.assertFalse(self.p91 <= self.p92)
        self.assertFalse(self.p92 <= self.p91)

        # Не пересекающиеся периоды, len(pA2) = 1
        self.assertFalse(self.pA1 <= self.pA2)
        self.assertFalse(self.pA2 <= self.pA1)

        # Не пересекающиеся периоды, len(pB2) = 1
        self.assertFalse(self.pB1 <= self.pB2)
        self.assertFalse(self.pB2 <= self.pB1)

        # Однодневные периоды, len(pC1) = len(pC2) = 1
        self.assertFalse(self.pC1 <= self.pC2)
        self.assertFalse(self.pC2 <= self.pC1)

        # Однодневные периоды равны, len(pC1) = 1
        self.assertFalse(self.pC1 <= self.pC1)

    def test_gt(self):
        """Тестирование __gt__ / >"""

        # ======================== Периоды ======================

        # Нет пересечения
        self.assertFalse(self.p11 > self.p12)
        self.assertTrue(self.p12 > self.p11)

        # Есть пересечение в несколько дней
        self.assertFalse(self.p21 > self.p22)
        self.assertFalse(self.p22 > self.p21)

        # Есть пересечение в один день
        self.assertFalse(self.p31 > self.p32)
        self.assertFalse(self.p32 > self.p31)

        # Периоды равны
        self.assertFalse(self.p21 > self.p21)

        # Вхождение периодов
        self.assertFalse(self.p41 > self.p42)
        self.assertFalse(self.p42 > self.p41)

        # !!!!!

        # Пересекающиеся периоды, пересечение в несколько дней, p51.begin = p52.begin
        self.assertFalse(self.p51 > self.p52)
        self.assertFalse(self.p52 > self.p51)

        # Пересекающиеся периоды, пересечение в несколько дней, p61.end = p62.end
        self.assertFalse(self.p61 > self.p62)
        self.assertFalse(self.p62 > self.p61)

        # Пересекающиеся периоды, p71.begin = p72.begin, len(p72) = 1
        self.assertFalse(self.p71 > self.p72)
        self.assertFalse(self.p72 > self.p71)

        # Пересекающиеся периоды, p81.end = p82.end, len(p82) = 1
        self.assertFalse(self.p81 > self.p82)
        self.assertFalse(self.p82 > self.p81)

        # Пересекающиеся периоды, len(p92) = 1
        self.assertFalse(self.p91 > self.p92)
        self.assertFalse(self.p92 > self.p91)

        # Не пересекающиеся периоды, len(pA2) = 1
        self.assertTrue(self.pA1 > self.pA2)
        self.assertFalse(self.pA2 > self.pA1)

        # Не пересекающиеся периоды, len(pB2) = 1
        self.assertFalse(self.pB1 > self.pB2)
        self.assertTrue(self.pB2 > self.pB1)

        # Однодневные периоды, len(pC1) = len(pC2) = 1
        self.assertFalse(self.pC1 > self.pC2)
        self.assertTrue(self.pC2 > self.pC1)

        # Однодневные периоды равны, len(pC1) = 1
        self.assertFalse(self.pC1 > self.pC1)

        # ======================== Даты ======================

        # Дата является началом периода
        self.assertFalse(self.p11 > self.p11.begin)
        # Дата является началом периода + 1 день
        self.assertFalse(self.p11 > self.p11.begin + datetime.timedelta(days=1))
        # Дата является началом периода - 1 день
        self.assertTrue(self.p11 > self.p11.begin - datetime.timedelta(days=1))
        # Дата является началом периода - 10 дней
        self.assertTrue(self.p11 > self.p11.begin - datetime.timedelta(days=10))

        # Дата является концом периода
        self.assertFalse(self.p11 > self.p11.end)
        # Дата является концом периода + 1 день
        self.assertFalse(self.p11 > self.p11.end + datetime.timedelta(days=1))
        # Дата является концом периода + 10 день
        self.assertFalse(self.p11 > self.p11.end + datetime.timedelta(days=10))
        # Дата является концом периода - 1 день
        self.assertFalse(self.p11 > self.p11.end - datetime.timedelta(days=1))

    def test_ge(self):
        """Тестирование __ge__ / >="""

        # ======================== Периоды ======================

        # Нет пересечения
        self.assertFalse(self.p11 >= self.p12)
        self.assertFalse(self.p12 >= self.p11)

        # Есть пересечение в несколько дней
        self.assertFalse(self.p21 >= self.p22)
        self.assertTrue(self.p22 >= self.p21)

        # Есть пересечение в один день
        self.assertFalse(self.p31 >= self.p32)
        self.assertTrue(self.p32 >= self.p31)

        # Периоды равны
        self.assertFalse(self.p21 >= self.p21)

        # Вхождение периодов
        self.assertFalse(self.p41 >= self.p42)
        self.assertFalse(self.p42 >= self.p41)

        # !!!!!

        # Пересекающиеся периоды, пересечение в несколько дней, p51.begin = p52.begin
        self.assertFalse(self.p51 >= self.p52)
        self.assertFalse(self.p52 >= self.p51)

        # Пересекающиеся периоды, пересечение в несколько дней, p61.end = p62.end
        self.assertFalse(self.p61 >= self.p62)
        self.assertFalse(self.p62 >= self.p61)

        # Пересекающиеся периоды, p71.begin = p72.begin, len(p72) = 1
        self.assertFalse(self.p71 >= self.p72)
        self.assertFalse(self.p72 >= self.p71)

        # Пересекающиеся периоды, p81.end = p82.end, len(p82) = 1
        self.assertFalse(self.p81 >= self.p82)
        self.assertFalse(self.p82 >= self.p81)

        # Пересекающиеся периоды, len(p92) = 1
        self.assertFalse(self.p91 >= self.p92)
        self.assertFalse(self.p92 >= self.p91)

        # Не пересекающиеся периоды, len(pA2) = 1
        self.assertFalse(self.pA1 >= self.pA2)
        self.assertFalse(self.pA2 >= self.pA1)

        # Не пересекающиеся периоды, len(pB2) = 1
        self.assertFalse(self.pB1 >= self.pB2)
        self.assertFalse(self.pB2 >= self.pB1)

        # Однодневные периоды, len(pC1) = len(pC2) = 1
        self.assertFalse(self.pC1 >= self.pC2)
        self.assertFalse(self.pC2 >= self.pC1)

        # Однодневные периоды равны, len(pC1) = 1
        self.assertFalse(self.pC1 >= self.pC1)

    def test_eq(self):
        """Тестирование __eq__ / =="""

        # ======================== Периоды ======================

        # Нет пересечения
        self.assertFalse(self.p11 == self.p12)
        self.assertFalse(self.p12 == self.p11)

        # Есть пересечение в несколько дней
        self.assertFalse(self.p21 == self.p22)
        self.assertFalse(self.p22 == self.p21)

        # Есть пересечение в один день
        self.assertFalse(self.p31 == self.p32)
        self.assertFalse(self.p32 == self.p31)

        # Периоды равны
        self.assertTrue(self.p21 == self.p21)

        # Вхождение периодов
        self.assertFalse(self.p41 == self.p42)
        self.assertFalse(self.p42 == self.p41)

        # !!!!!

        # Пересекающиеся периоды, пересечение в несколько дней, p51.begin = p52.begin
        self.assertFalse(self.p51 == self.p52)
        self.assertFalse(self.p52 == self.p51)

        # Пересекающиеся периоды, пересечение в несколько дней, p61.end = p62.end
        self.assertFalse(self.p61 == self.p62)
        self.assertFalse(self.p62 == self.p61)

        # Пересекающиеся периоды, p71.begin = p72.begin, len(p72) = 1
        self.assertFalse(self.p71 == self.p72)
        self.assertFalse(self.p72 == self.p71)

        # Пересекающиеся периоды, p81.end = p82.end, len(p82) = 1
        self.assertFalse(self.p81 == self.p82)
        self.assertFalse(self.p82 == self.p81)

        # Пересекающиеся периоды, len(p92) = 1
        self.assertFalse(self.p91 == self.p92)
        self.assertFalse(self.p92 == self.p91)

        # Не пересекающиеся периоды, len(pA2) = 1
        self.assertFalse(self.pA1 == self.pA2)
        self.assertFalse(self.pA2 == self.pA1)

        # Не пересекающиеся периоды, len(pB2) = 1
        self.assertFalse(self.pB1 == self.pB2)
        self.assertFalse(self.pB2 == self.pB1)

        # Однодневные периоды, len(pC1) = len(pC2) = 1
        self.assertFalse(self.pC1 == self.pC2)
        self.assertFalse(self.pC2 == self.pC1)

        # Однодневные периоды равны, len(pC1) = 1
        self.assertTrue(self.pC1 == self.pC1)

        # ======================== Даты ======================

        # Дата является началом периода
        self.assertFalse(self.p11 == self.p11.begin)
        # Дата является началом периода + 1 день
        self.assertFalse(self.p11 == self.p11.begin + datetime.timedelta(days=1))
        # Дата является началом периода - 1 день
        self.assertFalse(self.p11 == self.p11.begin - datetime.timedelta(days=1))
        # Дата является началом периода - 10 дней
        self.assertFalse(self.p11 == self.p11.begin - datetime.timedelta(days=10))

        # Дата является концом периода
        self.assertFalse(self.p11 == self.p11.end)
        # Дата является концом периода + 1 день
        self.assertFalse(self.p11 == self.p11.end + datetime.timedelta(days=1))
        # Дата является концом периода + 10 день
        self.assertFalse(self.p11 == self.p11.end + datetime.timedelta(days=10))
        # Дата является концом периода - 1 день
        self.assertFalse(self.p11 == self.p11.end - datetime.timedelta(days=1))

    def test_ne(self):
        """Тестирование __ne__ / !="""

        # ======================== Периоды ======================

        # Нет пересечения
        self.assertTrue(self.p11 != self.p12)
        self.assertTrue(self.p12 != self.p11)

        # Есть пересечение в несколько дней
        self.assertTrue(self.p21 != self.p22)
        self.assertTrue(self.p22 != self.p21)

        # Есть пересечение в один день
        self.assertTrue(self.p31 != self.p32)
        self.assertTrue(self.p32 != self.p31)

        # Периоды равны
        self.assertFalse(self.p21 != self.p21)

        # Вхождение периодов
        self.assertTrue(self.p41 != self.p42)
        self.assertTrue(self.p42 != self.p41)

        # !!!!!

        # Пересекающиеся периоды, пересечение в несколько дней, p51.begin = p52.begin
        self.assertTrue(self.p51 != self.p52)
        self.assertTrue(self.p52 != self.p51)

        # Пересекающиеся периоды, пересечение в несколько дней, p61.end = p62.end
        self.assertTrue(self.p61 != self.p62)
        self.assertTrue(self.p62 != self.p61)

        # Пересекающиеся периоды, p71.begin = p72.begin, len(p72) = 1
        self.assertTrue(self.p71 != self.p72)
        self.assertTrue(self.p72 != self.p71)

        # Пересекающиеся периоды, p81.end = p82.end, len(p82) = 1
        self.assertTrue(self.p81 != self.p82)
        self.assertTrue(self.p82 != self.p81)

        # Пересекающиеся периоды, len(p92) = 1
        self.assertTrue(self.p91 != self.p92)
        self.assertTrue(self.p92 != self.p91)

        # Не пересекающиеся периоды, len(pA2) = 1
        self.assertTrue(self.pA1 != self.pA2)
        self.assertTrue(self.pA2 != self.pA1)

        # Не пересекающиеся периоды, len(pB2) = 1
        self.assertTrue(self.pB1 != self.pB2)
        self.assertTrue(self.pB2 != self.pB1)

        # Однодневные периоды, len(pC1) = len(pC2) = 1
        self.assertTrue(self.pC1 != self.pC2)
        self.assertTrue(self.pC2 != self.pC1)

        # Однодневные периоды равны, len(pC1) = 1
        self.assertFalse(self.pC1 != self.pC1)

        # ======================== Даты ======================

        # Дата является началом периода
        self.assertTrue(self.p11 != self.p11.begin)
        # Дата является началом периода + 1 день
        self.assertTrue(self.p11 != self.p11.begin + datetime.timedelta(days=1))
        # Дата является началом периода - 1 день
        self.assertTrue(self.p11 != self.p11.begin - datetime.timedelta(days=1))
        # Дата является началом периода - 10 дней
        self.assertTrue(self.p11 != self.p11.begin - datetime.timedelta(days=10))

        # Дата является концом периода
        self.assertTrue(self.p11 != self.p11.end)
        # Дата является концом периода + 1 день
        self.assertTrue(self.p11 != self.p11.end + datetime.timedelta(days=1))
        # Дата является концом периода + 10 день
        self.assertTrue(self.p11 != self.p11.end + datetime.timedelta(days=10))
        # Дата является концом периода - 1 день
        self.assertTrue(self.p11 != self.p11.end - datetime.timedelta(days=1))

    # ---------------------------------------------Арифметические операторы------------------------------------

    def test_add(self):
        """Тестирование __add__ / +"""

        # ======================== Периоды ======================

        # Нет пересечения
        res1 = [self.p11, self.p12]
        self.assertListEqual(self.p11 + self.p12, res1)
        self.assertEqual((self.p11 + self.p12)[0].data, res1[0].data)
        self.assertEqual((self.p11 + self.p12)[1].data, res1[1].data)

        res2 = [self.p12, self.p11]
        self.assertListEqual(self.p12 + self.p11, res2)
        self.assertEqual((self.p12 + self.p11)[0].data, res2[0].data)
        self.assertEqual((self.p12 + self.p11)[1].data, res2[1].data)

        # Есть пересечение в несколько дней
        self.assertListEqual(self.p21 + self.p22, [DatePeriod(self.p21.begin, self.p22.end)])
        self.assertEqual((self.p21 + self.p22)[0].data, self.p21.data)

        self.assertListEqual(self.p22 + self.p21, [DatePeriod(self.p21.begin, self.p22.end)])
        self.assertEqual((self.p22 + self.p21)[0].data, self.p22.data)

        # Есть пересечение в один день
        self.assertListEqual(self.p31 + self.p32, [DatePeriod(self.p31.begin, self.p32.end)])
        self.assertEqual((self.p31 + self.p32)[0].data, self.p31.data)

        self.assertListEqual(self.p32 + self.p31, [DatePeriod(self.p31.begin, self.p32.end)])
        self.assertEqual((self.p32 + self.p31)[0].data, self.p32.data)

        # Периоды равны
        p21c = copy.copy(self.p21)
        p21c.data = 'p21c'

        self.assertListEqual(self.p21 + p21c, [DatePeriod(self.p21.begin, self.p21.end)])
        self.assertEqual((self.p21 + p21c)[0].data, self.p21.data)

        self.assertListEqual(p21c + self.p21, [DatePeriod(p21c.begin, p21c.end)])
        self.assertEqual((p21c + self.p21)[0].data, p21c.data)

        # Вхождение периодов
        self.assertListEqual(self.p41 + self.p42, [DatePeriod(self.p41.begin, self.p41.end)])
        self.assertEqual((self.p41 + self.p42)[0].data, self.p41.data)

        #
        # >>>>> Protected = False
        self.assertListEqual(self.p42 + self.p41, [DatePeriod(self.p41.begin, self.p41.end)])
        self.assertEqual((self.p42 + self.p41)[0].data, self.p41.data)

        # >>>>> Protected = True
        p42protected = copy.copy(self.p42)
        p42protected.protect_data = True
        self.assertListEqual(p42protected + self.p41, [DatePeriod(self.p41.begin, self.p41.end)])
        self.assertEqual((p42protected + self.p41)[0].data, p42protected.data)

        # !!!!!

        # Пересекающиеся периоды, пересечение в несколько дней, p51.begin = p52.begin
        self.assertListEqual(self.p51 + self.p52, [DatePeriod(self.p51.begin, self.p51.end)])
        self.assertEqual((self.p51 + self.p52)[0].data, self.p51.data)

        #

        # >>>>> Protected = False
        self.assertListEqual(self.p52 + self.p51, [DatePeriod(self.p51.begin, self.p51.end)])
        self.assertEqual((self.p52 + self.p51)[0].data, self.p51.data)

        # >>>>> Protected = True
        p52protected = copy.copy(self.p52)
        p52protected.protect_data = True
        self.assertListEqual(p52protected + self.p51, [DatePeriod(self.p51.begin, self.p51.end)])
        self.assertEqual((p52protected + self.p51)[0].data, p52protected.data)

        # Пересекающиеся периоды, пересечение в несколько дней, p61.end = p62.end
        self.assertListEqual(self.p61 + self.p62, [DatePeriod(self.p61.begin, self.p62.end)])
        self.assertEqual((self.p61 + self.p62)[0].data, self.p61.data)

        #

        # >>>>> Protected = False
        self.assertListEqual(self.p62 + self.p61, [DatePeriod(self.p61.begin, self.p61.end)])
        self.assertEqual((self.p62 + self.p61)[0].data, self.p61.data)

        # >>>>> Protected = True
        p62protected = copy.copy(self.p62)
        p62protected.protect_data = True
        self.assertListEqual(p62protected + self.p61, [DatePeriod(self.p61.begin, self.p61.end)])
        self.assertEqual((p62protected + self.p61)[0].data, p62protected.data)

        # Пересекающиеся периоды, p71.begin = p72.begin, len(p72) = 1
        self.assertListEqual(self.p71 + self.p72, [DatePeriod(self.p71.begin, self.p71.end)])
        self.assertEqual((self.p71 + self.p72)[0].data, self.p71.data)

        #

        # >>>>> Protected = False
        self.assertListEqual(self.p72 + self.p71, [DatePeriod(self.p71.begin, self.p71.end)])
        self.assertEqual((self.p72 + self.p71)[0].data, self.p71.data)

        # >>>>> Protected = True
        p72protected = copy.copy(self.p72)
        p72protected.protect_data = True
        self.assertListEqual(p72protected + self.p71, [DatePeriod(self.p71.begin, self.p71.end)])
        self.assertEqual((p72protected + self.p71)[0].data, p72protected.data)

        # Пересекающиеся периоды, p81.end = p82.end, len(p82) = 1
        self.assertListEqual(self.p81 + self.p82, [DatePeriod(self.p81.begin, self.p82.end)])
        self.assertEqual((self.p81 + self.p82)[0].data, self.p81.data)

        #

        # >>>>> Protected = False
        self.assertListEqual(self.p82 + self.p81, [DatePeriod(self.p81.begin, self.p81.end)])
        self.assertEqual((self.p82 + self.p81)[0].data, self.p81.data)

        # >>>>> Protected = True
        p82protected = copy.copy(self.p82)
        p82protected.protect_data = True
        self.assertListEqual(p82protected + self.p81, [DatePeriod(self.p81.begin, self.p81.end)])
        self.assertEqual((p82protected + self.p81)[0].data, p82protected.data)

        # Пересекающиеся периоды, len(p92) = 1
        self.assertListEqual(self.p91 + self.p92, [DatePeriod(self.p91.begin, self.p91.end)])
        self.assertEqual((self.p91 + self.p92)[0].data, self.p91.data)

        #

        # >>>>> Protected = False
        self.assertListEqual(self.p92 + self.p91, [DatePeriod(self.p91.begin, self.p91.end)])
        self.assertEqual((self.p92 + self.p91)[0].data, self.p91.data)

        # >>>>> Protected = True
        p92protected = copy.copy(self.p92)
        p92protected.protect_data = True
        self.assertListEqual(p92protected + self.p91, [DatePeriod(self.p91.begin, self.p91.end)])
        self.assertEqual((p92protected + self.p91)[0].data, p92protected.data)

        # Не пересекающиеся периоды, len(pA2) = 1
        res1 = [self.pA1, self.pA2]
        self.assertListEqual(self.pA1 + self.pA2, res1)
        self.assertEqual((self.pA1 + self.pA2)[0].data, res1[0].data)
        self.assertEqual((self.pA1 + self.pA2)[1].data, res1[1].data)

        res2 = [self.pA2, self.pA1]
        self.assertListEqual(self.pA2 + self.pA1, res2)
        self.assertEqual((self.pA2 + self.pA1)[0].data, res2[0].data)
        self.assertEqual((self.pA2 + self.pA1)[1].data, res2[1].data)

        # Не пересекающиеся периоды, len(pB2) = 1
        res1 = [self.pB1, self.pB2]
        self.assertListEqual(self.pB1 + self.pB2, res1)
        self.assertEqual((self.pB1 + self.pB2)[0].data, res1[0].data)
        self.assertEqual((self.pB1 + self.pB2)[1].data, res1[1].data)

        res2 = [self.pB2, self.pB1]
        self.assertListEqual(self.pB2 + self.pB1, res2)
        self.assertEqual((self.pB2 + self.pB1)[0].data, res2[0].data)
        self.assertEqual((self.pB2 + self.pB1)[1].data, res2[1].data)

        # Однодневные периоды, len(pC1) = len(pC2) = 1
        res1 = [self.pC1, self.pC2]
        self.assertListEqual(self.pC1 + self.pC2, res1)
        self.assertEqual((self.pC1 + self.pC2)[0].data, res1[0].data)
        self.assertEqual((self.pC1 + self.pC2)[1].data, res1[1].data)

        res2 = [self.pC2, self.pC1]
        self.assertListEqual(self.pC2 + self.pC1, res2)
        self.assertEqual((self.pC2 + self.pC1)[0].data, res2[0].data)
        self.assertEqual((self.pC2 + self.pC1)[1].data, res2[1].data)

        # Однодневные периоды равны, len(pC1) = 1
        pC1c = copy.copy(self.pC1)
        pC1c.data = 'pC1c'

        self.assertListEqual(self.pC1 + pC1c, [self.pC1])
        self.assertEqual((self.pC1 + pC1c)[0].data, self.pC1.data)

        self.assertListEqual(pC1c + self.pC1, [pC1c])
        self.assertEqual((pC1c + self.pC1)[0].data, pC1c.data)

    def test_sub(self):
        """Тестирование __sub__ / -"""

        # ======================== Периоды ======================

        # Нет пересечения
        self.assertListEqual(self.p11 - self.p12, [self.p11])
        self.assertEqual((self.p11 - self.p12)[0].data, self.p11.data)

        self.assertListEqual(self.p12 - self.p11, [self.p12])
        self.assertEqual((self.p12 - self.p11)[0].data, self.p12.data)

        # Есть пересечение в несколько дней
        self.assertListEqual(self.p21 - self.p22,
                             [DatePeriod(self.p21.begin, self.p22.begin - datetime.timedelta(days=1))])
        self.assertEqual((self.p21 - self.p22)[0].data, self.p21.data)

        self.assertListEqual(self.p22 - self.p21,
                             [DatePeriod(self.p21.end + datetime.timedelta(days=1), self.p22.end)])
        self.assertEqual((self.p22 - self.p21)[0].data, self.p22.data)

        # Есть пересечение в один день
        self.assertListEqual(self.p31 - self.p32,
                             [DatePeriod(self.p31.begin, self.p31.end - datetime.timedelta(days=1))])
        self.assertEqual((self.p31 - self.p32)[0].data, self.p31.data)

        self.assertListEqual(self.p32 - self.p31,
                             [DatePeriod(self.p32.begin + datetime.timedelta(days=1), self.p32.end)])
        self.assertEqual((self.p32 - self.p31)[0].data, self.p32.data)

        # Периоды равны
        p21c = copy.copy(self.p21)
        p21c.data = 'p21c'

        self.assertListEqual(self.p21 - p21c, [])
        self.assertListEqual(p21c - self.p21, [])

        # Вхождение периодов
        self.assertListEqual(self.p41 - self.p42, [
            DatePeriod(self.p41.begin, self.p42.begin - datetime.timedelta(days=1)),
            DatePeriod(self.p42.end + datetime.timedelta(days=1), self.p41.end),
        ])
        self.assertEqual((self.p41 - self.p42)[0].data, self.p41.data)
        self.assertEqual((self.p41 - self.p42)[1].data, self.p41.data)

        self.assertListEqual(self.p42 - self.p41, [])

        # !!!!!

        # Пересекающиеся периоды, пересечение в несколько дней, p51.begin = p52.begin
        self.assertListEqual(self.p51 - self.p52,
                             [DatePeriod(self.p52.end + datetime.timedelta(days=1), self.p51.end)])
        self.assertEqual((self.p51 - self.p52)[0].data, self.p51.data)

        self.assertListEqual(self.p52 - self.p51, [])

        # Пересекающиеся периоды, пересечение в несколько дней, p61.end = p62.end
        self.assertListEqual(self.p61 - self.p62,
                             [DatePeriod(self.p61.begin, self.p62.begin - datetime.timedelta(days=1))])
        self.assertEqual((self.p61 - self.p62)[0].data, self.p61.data)

        self.assertListEqual(self.p62 - self.p61, [])

        # Пересекающиеся периоды, p71.begin = p72.begin, len(p72) = 1
        self.assertListEqual(self.p71 - self.p72,
                             [DatePeriod(self.p72.begin + datetime.timedelta(days=1), self.p71.end)])
        self.assertEqual((self.p71 - self.p72)[0].data, self.p71.data)

        self.assertListEqual(self.p72 - self.p71, [])

        # Пересекающиеся периоды, p81.end = p82.end, len(p82) = 1
        self.assertListEqual(self.p81 - self.p82,
                             [DatePeriod(self.p81.begin, self.p82.end - datetime.timedelta(days=1))])
        self.assertEqual((self.p81 - self.p82)[0].data, self.p81.data)

        self.assertListEqual(self.p82 - self.p81, [])

        # Пересекающиеся периоды, len(p92) = 1
        self.assertListEqual(self.p91 - self.p92, [
            DatePeriod(self.p91.begin, self.p92.begin - datetime.timedelta(days=1)),
            DatePeriod(self.p92.end + datetime.timedelta(days=1), self.p91.end),
        ])
        self.assertEqual((self.p91 - self.p92)[0].data, self.p91.data)
        self.assertEqual((self.p91 - self.p92)[1].data, self.p91.data)

        self.assertListEqual(self.p92 - self.p91, [])

        # Не пересекающиеся периоды, len(pA2) = 1
        self.assertListEqual(self.pA1 - self.pA2, [DatePeriod(self.pA1.begin, self.pA1.end)])
        self.assertEqual((self.pA1 - self.pA2)[0].data, self.pA1.data)

        self.assertListEqual(self.pA2 - self.pA1, [DatePeriod(self.pA2.begin, self.pA2.end)])
        self.assertEqual((self.pA2 - self.pA1)[0].data, self.pA2.data)

        # Не пересекающиеся периоды, len(pB2) = 1
        self.assertListEqual(self.pB1 - self.pB2, [DatePeriod(self.pB1.begin, self.pB1.end)])
        self.assertEqual((self.pB1 - self.pB2)[0].data, self.pB1.data)

        self.assertListEqual(self.pB2 - self.pB1, [DatePeriod(self.pB2.begin, self.pB2.end)])
        self.assertEqual((self.pB2 - self.pB1)[0].data, self.pB2.data)

        # Однодневные периоды, len(pC1) = len(pC2) = 1
        self.assertListEqual(self.pC1 - self.pC2, [self.pC1])
        self.assertEqual((self.pC1 - self.pC2)[0].data, self.pC1.data)

        self.assertListEqual(self.pC2 - self.pC1, [self.pC2])
        self.assertEqual((self.pC2 - self.pC1)[0].data, self.pC2.data)

        # Однодневные периоды равны, len(pC1) = 1
        pC1c = copy.copy(self.pC1)
        pC1c.data = 'pC1c'

        self.assertListEqual(self.pC1 - pC1c, [])
        self.assertListEqual(pC1c - self.pC1, [])

    # ---------------------------------------------Остальные операторы------------------------------------

    def test_len(self):
        """Тестирование __len__ / len(self)"""
        self.assertEqual(len(self.p11), 25)
        self.assertEqual(len(self.p12), 25)
        self.assertEqual(len(self.p21), 31)
        self.assertEqual(len(self.p22), 36)
        self.assertEqual(len(self.p72), 1)

    def test_iter(self):
        """Тестирование __iter__ / iter(self)"""
        self.assertListEqual([x for x in DatePeriod(datetime.date(2020, 1, 3), datetime.date(2020, 1, 6))], [
            datetime.date(2020, 1, 3),
            datetime.date(2020, 1, 4),
            datetime.date(2020, 1, 5),
            datetime.date(2020, 1, 6),
        ])

        self.assertListEqual([x for x in DatePeriod(datetime.date(2020, 1, 3), datetime.date(2020, 1, 3))], [
            datetime.date(2020, 1, 3),
        ])

    # ---------------------------------------------Методы------------------------------------

    def test_split(self):
        """Тестирование метода split"""

        # ======================== Периоды ======================

        # Нет пересечения
        self.assertListEqual(self.p11.split(self.p12), [self.p11])
        self.assertEqual(self.p11.split(self.p12)[0].data, self.p11.data)

        self.assertListEqual(self.p12.split(self.p11), [self.p12])
        self.assertEqual(self.p12.split(self.p11)[0].data, self.p12.data)

        # Есть пересечение в несколько дней
        self.assertListEqual(self.p21.split(self.p22), [
            DatePeriod(self.p21.begin, self.p22.begin - datetime.timedelta(days=1)),
            DatePeriod(self.p22.begin, self.p21.end),
            DatePeriod(self.p21.end + datetime.timedelta(days=1), self.p22.end),
        ])
        self.assertEqual(self.p21.split(self.p22)[0].data, self.p21.data)
        self.assertEqual(self.p21.split(self.p22)[1].data, self.p21.data)
        self.assertEqual(self.p21.split(self.p22)[2].data, self.p21.data)

        #

        self.assertListEqual(self.p22.split(self.p21), [
            DatePeriod(self.p21.begin, self.p22.begin - datetime.timedelta(days=1)),
            DatePeriod(self.p22.begin, self.p21.end),
            DatePeriod(self.p21.end + datetime.timedelta(days=1), self.p22.end),
        ])
        self.assertEqual(self.p22.split(self.p21)[0].data, self.p22.data)
        self.assertEqual(self.p22.split(self.p21)[1].data, self.p22.data)
        self.assertEqual(self.p22.split(self.p21)[2].data, self.p22.data)

        # Есть пересечение в один день
        self.assertListEqual(self.p31.split(self.p32), [
            DatePeriod(self.p31.begin, self.p32.begin - datetime.timedelta(days=1)),
            DatePeriod(self.p32.begin, self.p31.end),
            DatePeriod(self.p31.end + datetime.timedelta(days=1), self.p32.end),
        ])
        self.assertEqual(self.p31.split(self.p32)[0].data, self.p31.data)
        self.assertEqual(self.p31.split(self.p32)[1].data, self.p31.data)
        self.assertEqual(self.p31.split(self.p32)[2].data, self.p31.data)

        #

        self.assertListEqual(self.p32.split(self.p31), [
            DatePeriod(self.p31.begin, self.p32.begin - datetime.timedelta(days=1)),
            DatePeriod(self.p32.begin, self.p31.end),
            DatePeriod(self.p31.end + datetime.timedelta(days=1), self.p32.end),
        ])
        self.assertEqual(self.p32.split(self.p31)[0].data, self.p32.data)
        self.assertEqual(self.p32.split(self.p31)[1].data, self.p32.data)
        self.assertEqual(self.p32.split(self.p31)[2].data, self.p32.data)

        # Периоды равны
        p21c = copy.copy(self.p21)
        p21c.data = 'p21c'

        self.assertListEqual(self.p21.split(p21c), [self.p21])

        # Вхождение периодов
        self.assertListEqual(self.p41.split(self.p42), [
            DatePeriod(self.p41.begin, self.p42.begin - datetime.timedelta(days=1)),
            DatePeriod(self.p42.begin, self.p42.end),
            DatePeriod(self.p42.end + datetime.timedelta(days=1), self.p41.end),
        ])
        self.assertEqual(self.p41.split(self.p42)[0].data, self.p41.data)
        self.assertEqual(self.p41.split(self.p42)[1].data, self.p41.data)
        self.assertEqual(self.p41.split(self.p42)[2].data, self.p41.data)

        self.assertListEqual(self.p42.split(self.p41), [self.p42])

        # !!!!!

        # Пересекающиеся периоды, пересечение в несколько дней, p51.begin = p52.begin
        self.assertListEqual(self.p51.split(self.p52), [
            DatePeriod(self.p52.begin, self.p52.end),
            DatePeriod(self.p52.end + datetime.timedelta(days=1), self.p51.end),
        ])
        self.assertEqual(self.p51.split(self.p52)[0].data, self.p51.data)
        self.assertEqual(self.p51.split(self.p52)[1].data, self.p51.data)

        #

        self.assertListEqual(self.p52.split(self.p51), [self.p52])

        # Пересекающиеся периоды, пересечение в несколько дней, p61.end = p62.end
        self.assertListEqual(self.p61.split(self.p62), [
            DatePeriod(self.p61.begin, self.p62.begin - datetime.timedelta(days=1)),
            DatePeriod(self.p62.begin, self.p62.end),
        ])
        self.assertEqual(self.p61.split(self.p62)[0].data, self.p61.data)
        self.assertEqual(self.p61.split(self.p62)[1].data, self.p61.data)

        #

        self.assertListEqual(self.p62.split(self.p61), [self.p62])

        # Пересекающиеся периоды, p71.begin = p72.begin, len(p72) = 1
        self.assertListEqual(self.p71.split(self.p72), [
            DatePeriod(self.p71.begin, self.p72.end),
            DatePeriod(self.p72.end + datetime.timedelta(days=1), self.p71.end),
        ])
        self.assertEqual(self.p71.split(self.p72)[0].data, self.p71.data)
        self.assertEqual(self.p71.split(self.p72)[1].data, self.p71.data)

        #

        self.assertListEqual(self.p72.split(self.p71), [self.p72])

        # Пересекающиеся периоды, p81.end = p82.end, len(p82) = 1
        self.assertListEqual(self.p81.split(self.p82), [
            DatePeriod(self.p81.begin, self.p82.begin - datetime.timedelta(days=1)),
            DatePeriod(self.p82.begin, self.p82.end),
        ])
        self.assertEqual(self.p81.split(self.p82)[0].data, self.p81.data)
        self.assertEqual(self.p81.split(self.p82)[1].data, self.p81.data)

        #

        self.assertListEqual(self.p82.split(self.p81), [self.p82])

        # Пересекающиеся периоды, len(p92) = 1
        self.assertListEqual(self.p91.split(self.p92), [
            DatePeriod(self.p91.begin, self.p92.begin - datetime.timedelta(days=1)),
            DatePeriod(self.p92.begin, self.p92.end),
            DatePeriod(self.p92.end + datetime.timedelta(days=1), self.p91.end),
        ])
        self.assertEqual(self.p91.split(self.p92)[0].data, self.p91.data)
        self.assertEqual(self.p91.split(self.p92)[1].data, self.p91.data)
        self.assertEqual(self.p91.split(self.p92)[2].data, self.p91.data)

        #

        self.assertListEqual(self.p92.split(self.p91), [self.p92])

        # Не пересекающиеся периоды, len(pA2) = 1
        self.assertListEqual(self.pA1.split(self.pA2), [DatePeriod(self.pA1.begin, self.pA1.end)])
        self.assertEqual(self.pA1.split(self.pA2)[0].data, self.pA1.data)

        #

        self.assertListEqual(self.pA2.split(self.pA1), [DatePeriod(self.pA2.begin, self.pA2.end)])
        self.assertEqual(self.pA2.split(self.pA1)[0].data, self.pA2.data)

        # Не пересекающиеся периоды, len(pB2) = 1
        self.assertListEqual(self.pB1.split(self.pB2), [DatePeriod(self.pB1.begin, self.pB1.end)])
        self.assertEqual(self.pB1.split(self.pB2)[0].data, self.pB1.data)

        #

        self.assertListEqual(self.pB2.split(self.pB1), [DatePeriod(self.pB2.begin, self.pB2.end)])
        self.assertEqual(self.pB2.split(self.pB1)[0].data, self.pB2.data)

        # Однодневные периоды, len(pC1) = len(pC2) = 1
        self.assertListEqual(self.pC1.split(self.pC2), [DatePeriod(self.pC1.begin, self.pC1.end)])
        self.assertEqual(self.pC1.split(self.pC2)[0].data, self.pC1.data)

        #

        self.assertListEqual(self.pC2.split(self.pC1), [DatePeriod(self.pC2.begin, self.pC2.end)])
        self.assertEqual(self.pC2.split(self.pC1)[0].data, self.pC2.data)

        # Однодневные периоды равны, len(pC1) = 1
        pC1c = copy.copy(self.pC1)
        pC1c.data = 'pC1c'

        self.assertListEqual(self.pC1.split(pC1c), [DatePeriod(self.pC1.begin, self.pC1.end)])
        self.assertEqual(self.pC1.split(pC1c)[0].data, self.pC1.data)

        #

        self.assertListEqual(pC1c.split(self.pC1), [DatePeriod(pC1c.begin, pC1c.end)])
        self.assertEqual(pC1c.split(self.pC1)[0].data, pC1c.data)

    def test_is_crossing(self):
        """Тестирование метода is_crossing"""

        # ======================== Периоды ======================

        # Нет пересечения
        self.assertFalse(self.p11.is_crossing(self.p12))
        self.assertFalse(self.p12.is_crossing(self.p11))

        # Есть пересечение в несколько дней
        self.assertTrue(self.p21.is_crossing(self.p22))
        self.assertTrue(self.p22.is_crossing(self.p21))

        # Есть пересечение в один день
        self.assertTrue(self.p31.is_crossing(self.p32))
        self.assertTrue(self.p32.is_crossing(self.p31))

        # Периоды равны
        self.assertTrue(self.p21.is_crossing(self.p21))

        # Вхождение периодов
        self.assertTrue(self.p41.is_crossing(self.p42))
        self.assertTrue(self.p42.is_crossing(self.p41))

        # !!!!!

        # Пересекающиеся периоды, пересечение в несколько дней, p51.begin = p52.begin
        self.assertTrue(self.p51.is_crossing(self.p52))
        self.assertTrue(self.p52.is_crossing(self.p51))

        # Пересекающиеся периоды, пересечение в несколько дней, p61.end = p62.end
        self.assertTrue(self.p61.is_crossing(self.p62))
        self.assertTrue(self.p62.is_crossing(self.p61))

        # Пересекающиеся периоды, p71.begin = p72.begin, len(p72) = 1
        self.assertTrue(self.p71.is_crossing(self.p72))
        self.assertTrue(self.p72.is_crossing(self.p71))

        # Пересекающиеся периоды, p81.end = p82.end, len(p82) = 1
        self.assertTrue(self.p81.is_crossing(self.p82))
        self.assertTrue(self.p82.is_crossing(self.p81))

        # Пересекающиеся периоды, len(p92) = 1
        self.assertTrue(self.p91.is_crossing(self.p92))
        self.assertTrue(self.p92.is_crossing(self.p91))

        # Не пересекающиеся периоды, len(pA2) = 1
        self.assertFalse(self.pA1.is_crossing(self.pA2))
        self.assertFalse(self.pA2.is_crossing(self.pA1))

        # Не пересекающиеся периоды, len(pB2) = 1
        self.assertFalse(self.pB1.is_crossing(self.pB2))
        self.assertFalse(self.pB2.is_crossing(self.pB1))

        # Однодневные периоды, len(pC1) = len(pC2) = 1
        self.assertFalse(self.pC1.is_crossing(self.pC2))
        self.assertFalse(self.pC2.is_crossing(self.pC1))

        # Однодневные периоды равны, len(pC1) = 1
        self.assertTrue(self.pC1.is_crossing(self.pC1))

    def test_crossing(self):
        """Тестирование метода crossing"""

        # ======================== Периоды ======================

        # Нет пересечения
        self.assertIsNone(self.p11.crossing(self.p12))

        self.assertIsNone(self.p12.crossing(self.p11))

        # Есть пересечение в несколько дней
        self.assertEqual(self.p21.crossing(self.p22), DatePeriod(self.p22.begin, self.p21.end))
        self.assertEqual(self.p21.crossing(self.p22).data, self.p21.data)

        #

        self.assertEqual(self.p22.crossing(self.p21), DatePeriod(self.p22.begin, self.p21.end))
        self.assertEqual(self.p22.crossing(self.p21).data, self.p22.data)

        # Есть пересечение в один день
        self.assertEqual(self.p31.crossing(self.p32), DatePeriod(self.p31.end, self.p32.begin))
        self.assertEqual(self.p31.crossing(self.p32), DatePeriod(self.p32.begin, self.p32.begin))
        self.assertEqual(self.p31.crossing(self.p32), DatePeriod(self.p31.end, self.p31.end))
        # Smorc

        self.assertEqual(self.p31.crossing(self.p32).data, self.p31.data)

        #

        self.assertEqual(self.p32.crossing(self.p31), DatePeriod(self.p31.end, self.p32.begin))
        self.assertEqual(self.p32.crossing(self.p31), DatePeriod(self.p32.begin, self.p32.begin))
        self.assertEqual(self.p32.crossing(self.p31), DatePeriod(self.p31.end, self.p31.end))
        # Smorc

        self.assertEqual(self.p32.crossing(self.p31).data, self.p32.data)

        # Периоды равны
        p21c = copy.copy(self.p21)
        p21c.data = 'p21c'

        self.assertEqual(self.p21.crossing(p21c), self.p21)
        self.assertEqual(self.p21.crossing(p21c).data, self.p21.data)

        self.assertEqual(p21c.crossing(self.p21), p21c)
        self.assertEqual(p21c.crossing(self.p21).data, p21c.data)

        # Вхождение периодов
        self.assertEqual(self.p41.crossing(self.p42), DatePeriod(self.p42.begin, self.p42.end))
        self.assertEqual(self.p41.crossing(self.p42).data, self.p41.data)

        self.assertEqual(self.p42.crossing(self.p41), DatePeriod(self.p42.begin, self.p42.end))
        self.assertEqual(self.p42.crossing(self.p41).data, self.p42.data)

        # !!!!!

        # Пересекающиеся периоды, пересечение в несколько дней, p51.begin = p52.begin
        self.assertEqual(self.p51.crossing(self.p52), DatePeriod(self.p52.begin, self.p52.end))
        self.assertEqual(self.p51.crossing(self.p52).data, self.p51.data)

        #

        self.assertEqual(self.p52.crossing(self.p51), DatePeriod(self.p52.begin, self.p52.end))
        self.assertEqual(self.p52.crossing(self.p51).data, self.p52.data)

        # Пересекающиеся периоды, пересечение в несколько дней, p61.end = p62.end
        self.assertEqual(self.p61.crossing(self.p62), DatePeriod(self.p62.begin, self.p62.end))
        self.assertEqual(self.p61.crossing(self.p62).data, self.p61.data)

        #

        self.assertEqual(self.p62.crossing(self.p61), DatePeriod(self.p62.begin, self.p62.end))
        self.assertEqual(self.p62.crossing(self.p61).data, self.p62.data)

        # Пересекающиеся периоды, p71.begin = p72.begin, len(p72) = 1
        self.assertEqual(self.p71.crossing(self.p72), DatePeriod(self.p72.begin, self.p72.end))
        self.assertEqual(self.p71.crossing(self.p72).data, self.p71.data)

        #

        self.assertEqual(self.p72.crossing(self.p71), DatePeriod(self.p72.begin, self.p72.end))
        self.assertEqual(self.p72.crossing(self.p71).data, self.p72.data)

        # Пересекающиеся периоды, p81.end = p82.end, len(p82) = 1
        self.assertEqual(self.p81.crossing(self.p82), DatePeriod(self.p82.begin, self.p82.end))
        self.assertEqual(self.p81.crossing(self.p82).data, self.p81.data)

        #

        self.assertEqual(self.p82.crossing(self.p81), DatePeriod(self.p82.begin, self.p82.end))
        self.assertEqual(self.p82.crossing(self.p81).data, self.p82.data)

        # Пересекающиеся периоды, len(p92) = 1
        self.assertEqual(self.p91.crossing(self.p92), DatePeriod(self.p92.begin, self.p92.end))
        self.assertEqual(self.p91.crossing(self.p92).data, self.p91.data)

        #

        self.assertEqual(self.p92.crossing(self.p91), DatePeriod(self.p92.begin, self.p92.end))
        self.assertEqual(self.p92.crossing(self.p91).data, self.p92.data)

        # Не пересекающиеся периоды, len(pA2) = 1
        self.assertIsNone(self.pA1.crossing(self.pA2))
        self.assertIsNone(self.pA2.crossing(self.pA1))

        # Не пересекающиеся периоды, len(pB2) = 1
        self.assertIsNone(self.pB1.crossing(self.pB2))
        self.assertIsNone(self.pB2.crossing(self.pB1))

        # Однодневные периоды, len(pC1) = len(pC2) = 1
        self.assertIsNone(self.pC1.crossing(self.pC2))
        self.assertIsNone(self.pC2.crossing(self.pC1))

        # Однодневные периоды равны, len(pC1) = 1
        pC1c = copy.copy(self.pC1)
        pC1c.data = 'pC1c'

        self.assertEqual(self.pC1.crossing(pC1c), self.pC1)
        self.assertEqual(self.pC1.crossing(pC1c).data, self.pC1.data)

        self.assertEqual(pC1c.crossing(self.pC1), pC1c)
        self.assertEqual(pC1c.crossing(self.pC1).data, pC1c.data)


class CircleSubTest(unittest.TestCase):
    """
    Тестирование циклического вычетания периодов

    p11 (DatePeriod):        |====================================================|                 # 01.02.2020 - 31.07.2020
    p12 (DatePeriod):             |=======|                                                         # 15.02.2020 - 25.02.2020
    p13 (DatePeriod):    |=======|                                                                  # 01.01.2020 - 14.02.2020
    p14 (DatePeriod):                                 |=======|                                     # 01.04.2020 - 20.04.2020
    p15 (DatePeriod):                       |=============|                                         # 01.03.2020 - 05.04.2020
    p16 (DatePeriod):                                                                  |=======|    # 15.08.2020 - 31.08.2020

    1) circle_sub( [p11], [p12, p13, p14, p15, p16])
    res (List): [
        26.02.2020 - 29.02.2020,
        21.04.2020 - 31.07.2020
    ]

    2) circle_sub( [p11], [p12, p14])
    res (List): [
        01.02.2020 - 14.02.2020,
        26.02.2020 - 31.03.2020,
        21.04.2020 - 31.07.2020
    ]

    3) circle_sub( [p11], [p16])
    res (List): [
        01.02.2020 - 31.07.2020
    ]

    4) circle_sub( [p11], [])
    res (List): [
        01.02.2020 - 31.07.2020
    ]

    5) circle_sub( [p12, p13, p14], [p15])
    res (List): [
        15.02.2020 - 25.02.2020,
        01.01.2020 - 14.02.2020,
        06.04.2020 - 20.04.2020
    ]

    6) circle_sub( [p12, p13, p14], [p11])
    res (List): [
        01.01.2020 - 31.01.2020
    ]
    """

    def setUp(self):
        self.p11 = DatePeriod(datetime.date(2020, 2, 1), datetime.date(2020, 7, 31), data='p11')
        self.p12 = DatePeriod(datetime.date(2020, 2, 15), datetime.date(2020, 2, 25), data='p12')
        self.p13 = DatePeriod(datetime.date(2020, 1, 1), datetime.date(2020, 2, 14), data='p13')
        self.p14 = DatePeriod(datetime.date(2020, 4, 1), datetime.date(2020, 4, 20), data='p14')
        self.p15 = DatePeriod(datetime.date(2020, 3, 1), datetime.date(2020, 4, 5), data='p15')
        self.p16 = DatePeriod(datetime.date(2020, 8, 15), datetime.date(2020, 8, 31), data='p16')

    # -------------------------------------------Условные операторы-----------------------------------------

    def test_main(self):
        # 1)
        self.assertListEqual(DatePeriod.circle_sub([self.p11], [self.p12, self.p13, self.p14, self.p15, self.p16]), [
            DatePeriod(datetime.date(2020, 2, 26), datetime.date(2020, 2, 29)),
            DatePeriod(datetime.date(2020, 4, 21), datetime.date(2020, 7, 31)),
        ])

        # 2)
        self.assertListEqual(DatePeriod.circle_sub([self.p11], [self.p12, self.p14]), [
            DatePeriod(datetime.date(2020, 2, 1), datetime.date(2020, 2, 14)),
            DatePeriod(datetime.date(2020, 2, 26), datetime.date(2020, 3, 31)),
            DatePeriod(datetime.date(2020, 4, 21), datetime.date(2020, 7, 31)),
        ])

        # 3)
        self.assertListEqual(DatePeriod.circle_sub([self.p11], [self.p16]), [
            DatePeriod(datetime.date(2020, 2, 1), datetime.date(2020, 7, 31)),
        ])

        # 4)
        self.assertListEqual(DatePeriod.circle_sub([self.p11], []), [
            DatePeriod(datetime.date(2020, 2, 1), datetime.date(2020, 7, 31)),
        ])

        # 5)
        self.assertListEqual(DatePeriod.circle_sub([self.p12, self.p13, self.p14], [self.p15]), [
            DatePeriod(datetime.date(2020, 2, 15), datetime.date(2020, 2, 25)),
            DatePeriod(datetime.date(2020, 1, 1), datetime.date(2020, 2, 14)),
            DatePeriod(datetime.date(2020, 4, 6), datetime.date(2020, 4, 20)),
        ])

        # 6)
        self.assertListEqual(DatePeriod.circle_sub([self.p12, self.p13, self.p14], [self.p11]), [
            DatePeriod(datetime.date(2020, 1, 1), datetime.date(2020, 1, 31)),
        ])

        # Проверка сортировки
        # 1)
        self.assertListEqual(sorted(DatePeriod.circle_sub([self.p12, self.p13, self.p14], [self.p15]), key=lambda x: x.begin),
                             [
                                 DatePeriod(datetime.date(2020, 1, 1), datetime.date(2020, 2, 14)),
                                 DatePeriod(datetime.date(2020, 2, 15), datetime.date(2020, 2, 25)),
                                 DatePeriod(datetime.date(2020, 4, 6), datetime.date(2020, 4, 20)),
                             ])

        deb = DatePeriod.circle_sub([self.p12, self.p13, self.p14], [self.p15])
        deb.sort(key=lambda x: x.begin)
        self.assertListEqual(deb, [
            DatePeriod(datetime.date(2020, 1, 1), datetime.date(2020, 2, 14)),
            DatePeriod(datetime.date(2020, 2, 15), datetime.date(2020, 2, 25)),
            DatePeriod(datetime.date(2020, 4, 6), datetime.date(2020, 4, 20)),
        ])

        # 2)
        # res = [p13, p11, p12, p15, p14, p16]
        self.assertListEqual(
            sorted([self.p11, self.p12, self.p13, self.p14, self.p15, self.p16], key=lambda x: x.begin),
            [self.p13, self.p11, self.p12, self.p15, self.p14, self.p16])

        deb = [self.p11, self.p12, self.p13, self.p14, self.p15, self.p16]
        deb.sort(key=lambda x: x.begin)
        self.assertListEqual(deb, [self.p13, self.p11, self.p12, self.p15, self.p14, self.p16])


class CircleCrossingTest(unittest.TestCase):
    """
    Тестирование циклического пересечения периодов.

    p11 (DatePeriod):        |====================================================|                 # 01.02.2020 - 31.07.2020
    p12 (DatePeriod):             |=======|                                                         # 15.02.2020 - 25.02.2020
    p13 (DatePeriod):    |=======|                                                                  # 01.01.2020 - 14.02.2020
    p14 (DatePeriod):                                 |=======|                                     # 01.04.2020 - 20.04.2020
    p15 (DatePeriod):                       |=============|                                         # 01.03.2020 - 05.04.2020
    p16 (DatePeriod):                                                                  |=======|    # 15.08.2020 - 31.08.2020

    1) circle_crossing( [p11], [p12, p13, p14, p15, p16])
    res (List) sorted: [
        01.02.2020 - 14.02.2020,
        15.02.2020 - 25.02.2020,
        01.03.2020 - 05.04.2020,
        01.04.2020 - 20.04.2020,
    ]
    """

    def setUp(self):
        self.p11 = DatePeriod(datetime.date(2020, 2, 1), datetime.date(2020, 7, 31), data='p11')
        self.p12 = DatePeriod(datetime.date(2020, 2, 15), datetime.date(2020, 2, 25), data='p12')
        self.p13 = DatePeriod(datetime.date(2020, 1, 1), datetime.date(2020, 2, 14), data='p13')
        self.p14 = DatePeriod(datetime.date(2020, 4, 1), datetime.date(2020, 4, 20), data='p14')
        self.p15 = DatePeriod(datetime.date(2020, 3, 1), datetime.date(2020, 4, 5), data='p15')
        self.p16 = DatePeriod(datetime.date(2020, 8, 15), datetime.date(2020, 8, 31), data='p16')

    # -------------------------------------------Условные операторы-----------------------------------------

    def test_main(self):
        # 1)
        self.assertListEqual(sorted(DatePeriod.circle_crossing([self.p11], [self.p12, self.p13, self.p14, self.p15]),
                                    key=lambda x: x.begin), [
            DatePeriod(datetime.date(2020, 2, 1), datetime.date(2020, 2, 14)),
            DatePeriod(datetime.date(2020, 2, 15), datetime.date(2020, 2, 25)),
            DatePeriod(datetime.date(2020, 3, 1), datetime.date(2020, 4, 5)),
            DatePeriod(datetime.date(2020, 4, 1), datetime.date(2020, 4, 20)),
                             ])


class CircleAddTest(unittest.TestCase):
    """
    Тестирование циклического сложения периодов.

    p11 (DatePeriod):     |===============|                                           # 01.02.2020 - 31.03.2020
    p12 (DatePeriod):                |===========================================|    # 05.03.2020 - 31.08.2020
    p13 (DatePeriod):                             |=======|                           # 01.05.2020 - 31.05.2020
    p14 (DatePeriod):                                  |=========================|    # 05.05.2020 - 31.08.2020
    p15 (DatePeriod):                                                  |======|       # 25.07.2020 - 20.08.2020

    1) circle_add( [p11], [p12, p13, p14, p15, p16])
    res (List): [
        01.02.2020 - 31.08.2020,
        01.02.2020 - 31.03.2020,
        01.05.2020 - 31.05.2020,
        01.02.2020 - 31.03.2020,
        05.05.2020 - 31.08.2020,
        01.02.2020 - 31.03.2020,
        25.07.2020 - 20.08.2020,
    ]
    """

    def setUp(self) -> None:
        self.p11 = DatePeriod(datetime.date(2020, 2, 1), datetime.date(2020, 3, 31), data='p11')
        self.p12 = DatePeriod(datetime.date(2020, 3, 5), datetime.date(2020, 8, 31), data='p12')
        self.p13 = DatePeriod(datetime.date(2020, 5, 1), datetime.date(2020, 5, 31), data='p13')
        self.p14 = DatePeriod(datetime.date(2020, 5, 5), datetime.date(2020, 8, 31), data='p14')
        self.p15 = DatePeriod(datetime.date(2020, 7, 25), datetime.date(2020, 8, 20), data='p15')

    # -------------------------------------------Условные операторы-----------------------------------------

    def test_main(self):
        # 1)
        deb = DatePeriod.circle_add([self.p11], [self.p12, self.p13, self.p14, self.p15])
        self.assertListEqual(DatePeriod.circle_add([self.p11], [self.p12, self.p13, self.p14, self.p15]), [
            DatePeriod(datetime.date(2020, 2, 1), datetime.date(2020, 8, 31)),
            DatePeriod(datetime.date(2020, 2, 1), datetime.date(2020, 3, 31)),
            DatePeriod(datetime.date(2020, 5, 1), datetime.date(2020, 5, 31)),
            DatePeriod(datetime.date(2020, 2, 1), datetime.date(2020, 3, 31)),
            DatePeriod(datetime.date(2020, 5, 5), datetime.date(2020, 8, 31)),
            DatePeriod(datetime.date(2020, 2, 1), datetime.date(2020, 3, 31)),
            DatePeriod(datetime.date(2020, 7, 25), datetime.date(2020, 8, 20)),
        ])

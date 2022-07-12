import itertools
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Generator, List, Tuple


class CyclicIterator:
    def __init__(self, iterable):
        self.iterable = itertools.cycle(iterable)

    def __iter__(self):
        return self.iterable

    def __next__(self):
        return next(self.iterable)


cyclic_iterator = CyclicIterator(range(3))
for i, j in enumerate(cyclic_iterator):
    print(j)
    if i == 20:
        break


@dataclass
class Movie:
    title: str
    dates: List[Tuple[datetime, datetime]]

    def schedule(self) -> Generator[datetime, None, None]:
        for period in self.dates:
            duration = (period[1] - period[0]).days + 1
            for days_count in range(duration):
                yield period[0] + timedelta(days=days_count)
        return []


m = Movie('sw', [
    (datetime(2020, 1, 1), datetime(2020, 1, 7)),
    (datetime(2020, 1, 15), datetime(2020, 2, 7))
])

for d in m.schedule():
    print(d)


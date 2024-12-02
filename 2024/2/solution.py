# %%
# Input parsing

path = 'inputs/test.txt'

with open(path, 'r') as file:
    lines = file.readlines()

reports = [list(map(int, line.split())) for line in lines]

# %%
# Task 1

from itertools import pairwise
from typing import Iterator


def check_reports(reports: list[list[int]]) -> Iterator[bool]:
    for report in reports:
        prev = 0
        for left, right in pairwise(report):
            curr = left - right

            # compare sign (increasing/decreasing)
            if prev * curr < 0:
                yield False
                break

            # compare difference (min 1, max 3)
            if abs(curr) < 1 or abs(curr) > 3:
                yield False
                break

            prev = curr
        else:
            yield True


result = list(check_reports(reports))
# print(result)
print('Result: ', sum(result))

# %%
# Task 2

from itertools import pairwise
from typing import Iterator


def check_reports(reports: list[list[int]]) -> Iterator[bool]:
    for i, report in enumerate(reports, start=1):
        result = check_report(report)
        yield result


def check_report(report: list[int], allow_remove: int = 1) -> bool:
    prev = 0
    for i, (left, right) in enumerate(pairwise(report)):
        curr = left - right

        check_signs = prev * curr < 0
        check_diff = abs(curr) < 1 or abs(curr) > 3

        if check_signs or check_diff:
            if not allow_remove:
                return False

            return (
                (
                    check_report(report[1:], allow_remove - 1)  # sign change
                    if i == 1
                    else False
                )
                or check_report(report[:i] + report[i + 1 :], allow_remove - 1)
                or check_report(
                    report[: i + 1] + report[i + 2 :], allow_remove - 1
                )
            )
        prev = curr
    return True


result = list(check_reports(reports))
# print(result)
print('Result:', sum(result))

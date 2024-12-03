# %%
# Input parsing

path = 'inputs/test.txt'

with open(path, 'r') as file:
    content = file.read()

# %%
# Task 1

import re
import operator


def find_mul(content: str):
    matches = re.findall(r'mul\((\d{1,3},\d{1,3})\)', content)
    return [
        operator.mul(*list(map(int, match.split(',')))) for match in matches
    ]


result = find_mul(content)
print('Result:', sum(result))

#%%
# Task 2

def with_blocker(content : str):
    matches = ['do()', *re.split(r'(don\'t\(\)|do\(\))', content)]

    return [
        result
        for op, text in zip(matches[::2], matches[1::2]) if op == 'do()'
        for result in find_mul(text)
    ]

result = with_blocker(content)
print('Result:', sum(result))
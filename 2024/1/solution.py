# %%

# Input parsing

path = 'inputs/test.txt'

with open(path, 'r') as file:
    contents = file.readlines()

left, right = list(map(list, zip(*[line.split() for line in contents])))
sorted_left, sorted_right = sorted(left), sorted(right)

# %%
## Task 1

diffs = [abs(int(l) - int(r)) for l, r in zip(sorted_left, sorted_right)]
print('Result: ', sum(diffs))

# %%
## Task 2


def count_items(items: list[str]) -> dict[str, int]:
    counter: dict[str, int] = {}
    for item in items:
        count = counter.get(item, 0)
        counter[item] = count + 1

    return counter


counter = count_items(right)


def calculate_similarity(left: list[str], right: list[str]) -> int:
    counter_left, counter_right = count_items(left), count_items(right)

    return sum(
        [int(k) * v * counter_right.get(k, 0) for k, v in counter_left.items()]
    )


similarity = calculate_similarity(left, right)
print('Result: ', similarity)

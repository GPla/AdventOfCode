# %%
from collections import defaultdict

with open("inputs/test.txt") as file:
    contents = file.read()
sequences = contents.split(",")


def hash(seq: str) -> int:
    current_value = 0
    for char in seq:
        current_value += ord(char)
        current_value *= 17
        current_value = current_value % 256
    return current_value


result = sum([hash(seq) for seq in sequences])

print("Part 1")
print("Answer:", result)

labels = defaultdict(list)
focal_lengths = defaultdict(list)

for seq in sequences:
    operator = '-' if '-' in seq else '='
    label = seq.split(operator)[0]
    box_number = hash(label)

    match operator:
        case "=":
            focal = int(seq.split(operator)[1])

            if label in labels[box_number]:
                index = labels[box_number].index(label)
                focal_lengths[box_number][index] = focal
            else:
                labels[box_number].append(label)
                focal_lengths[box_number].append(focal)
        case "-":
            if label not in labels[box_number]:
                continue

            index = labels[box_number].index(label)
            labels[box_number].pop(index)
            focal_lengths[box_number].pop(index)


def calculate_focusing_power(focal_lengths: dict[int, list[str]]):
    return sum(
        [
            (box_number + 1) * i * length
            for box_number, lengths in focal_lengths.items()
            for i, length in enumerate(lengths, 1)
        ]
    )


fp = calculate_focusing_power(dict(focal_lengths))

print("Part 2")
print("Answer:", fp)

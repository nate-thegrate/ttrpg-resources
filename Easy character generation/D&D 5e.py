Determining_Stats = False
# set false to just display info

True_Random = False

arrays = [
    [18, 17,  8,  8,  7,  7],
    [18, 15, 14,  7,  7,  7],
    [18, 14, 13, 11,  7,  7],
    [18, 11, 11, 11, 11, 11],
    [17, 16, 10, 10,  9,  9],
    [17, 14, 12, 10, 10, 10],
    [16, 16, 16,  7,  7,  7],
    [16, 15, 14, 10,  8,  8],
    [16, 14, 13, 12, 10,  9],
    [16, 12, 12, 12, 12, 12],
    [15, 14, 14, 14,  9,  9],
    [15, 15, 15, 10, 10, 10],
    [15, 14, 12, 12, 12, 12],
    [14, 14, 14, 14, 14,  9]
]

from random import *

def cheat(array):
    if random() > 12/13:  # Barbarian
        better_stats = [0, 1, 2]
    else:
        str_dex = int(random() + 0.75)
        con = 2
        x = random()
        int_wis_cha = 3 if x < 2/9 else 4 if x < 2/3 else 5
        better_stats = [str_dex, con, int_wis_cha]
    output = array[3:]
    better_values = array[:3]
    shuffle(better_values)
    shuffle(output)
    for stat in better_stats:
        output.insert(stat, better_values.pop(0))
    return output


if Determining_Stats:
    array = choice(arrays)
    if True_Random:
        shuffle(array)
    else:
        array = cheat(array)
    stats = [
        "Strength    ",
        "Dexterity   ",
        "Constitution",
        "Intelligence",
        "Wisdom      ",
        "Charisma    "
    ]
    for i in range(len(stats)):
        print(stats[i], array[i])
else:
    for array in arrays:
        print("\nArray: ", end="")
        for num in array:
            print(num, end=" ")
        print("\nMean:", round(sum(array) / len(array), 1))
        print("Highest mod: +", int(array[0] / 2 - 4), sep="")
        second_highest = int(array[1] / 2 - 4) if array[0] % 2 == 1 or array[1] % 2 == 1 \
                         else int(array[1] / 2 - 5)
        print("2nd highest: +", second_highest, sep="")
        # mods are calculated after race ASIs,
        # assuming a +2 and +1 are applied to highest stats

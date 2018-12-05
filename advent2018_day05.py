# Wow.  For some reason, my usual method of just pasting the input as a string literal in Python resulted
# in completely bonkers memory consumption to the tune of gigabytes.  If I read from a file, everything's fine.
INPUT = open("advent2018_day5_input.txt", "r").readlines()[0].strip()

def react_polymer(polymer, filter=None):
    i = 0
    remove_count = 0
    cur_polymer = polymer
    if filter:
        cur_polymer = cur_polymer.replace(filter.lower(), '')
        cur_polymer = cur_polymer.replace(filter.upper(), '')
    while True:
        if i >= len(cur_polymer) - 1:
            break
        if cur_polymer[i] != cur_polymer[i+1] and cur_polymer[i].lower() == cur_polymer[i+1].lower():
            cur_polymer = cur_polymer[:i] + cur_polymer[i + 2:]
            remove_count += 1
            # Resume scanning from one character back
            if i > 0:
                i -= 1
            continue
        i += 1
    return cur_polymer

result = react_polymer(INPUT)

print("Remaining polymer with length %d is %s" % (len(result), result))

length_dict = {}
for char in "abcdefghijklmnopqrstuvwxyz":
    result = react_polymer(INPUT, filter=char)
    length_dict[char] = len(result)

shortest = min(length_dict, key=length_dict.get)
print("Shortest reaction is %s, with a length of %d" % (shortest, length_dict[shortest]))


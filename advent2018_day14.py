INPUT = '306281'


# Not strictly needed, but was useful for debugging
def recipes_str(recipes, elf_positions):
    recipe_list = ''
    for i in xrange(len(recipes)):
        if i == elf_positions[0] and i == elf_positions[1]:
            recipe_list += '(%d]' % recipes[i]
        elif i == elf_positions[0]:
            recipe_list += '(%d)' % recipes[i]
        elif i == elf_positions[1]:
            recipe_list += '[%d]' % recipes[i]
        else:
            recipe_list += ' %d ' % recipes[i]
    return recipe_list


def add_recipes(recipes, elf_positions):
    found_input = None
    for digit in str(sum([int(recipes[x]) for x in elf_positions])):
        recipes.append(digit)
        if ''.join(recipes[-len(INPUT):]) == INPUT:
            found_input = len(recipes) - len(INPUT)

    for i, position in enumerate(elf_positions):
        elf_positions[i] = (position + int(recipes[position]) + 1) % len(recipes)

    return found_input


def part_one():
    elf_positions = [0, 1]
    recipes = ['3', '7']
    while len(recipes) <= int(INPUT) + 10:
        add_recipes(recipes, elf_positions)
    return ''.join(recipes[int(INPUT):int(INPUT)+10])


def part_two():
    elf_positions = [0, 1]
    recipes = ['3', '7']
    while True:
        found_input = add_recipes(recipes, elf_positions)
        if found_input:
            return found_input

print("Score of the ten recipes following the first %s recipes: %s" % (INPUT, part_one()))
print("Number of recipes that occur before %s: %s" % (INPUT, part_two()))

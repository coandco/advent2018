import re
IMMUNE, INFECTION = open("advent2018_day24_input.txt", "r").read().split("\n\n")
IMMUNE = IMMUNE.split("\n")[1:]
INFECTION = INFECTION.split("\n")[1:]

ALTIMMUNE, ALTINFECTION = """Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
"""[:-1].split("\n\n")

ALTIMMUNE = ALTIMMUNE.split("\n")[1:]
ALTINFECTION = ALTINFECTION.split("\n")[1:]


MAIN_REGEX_STR = r'(?P<num_units>\d+) units each with (?P<hp>\d+) hit points (?:\((?P<modifiers>[^)]+)\) )?with an attack that does (?P<atk>\d+) (?P<dmg_type>[^ ]+) damage at initiative (?P<init>\d+)'
MAIN_REGEX = re.compile(MAIN_REGEX_STR)

WEAKNESS_REGEX_STR = r'(?P<modifier_type>[a-z]+) to (?P<dmg_type_list>[a-z, ]+)'
WEAKNESS_REGEX = re.compile(WEAKNESS_REGEX_STR)

# Damage types
FIRE = 0
COLD = 1
BLUDGEONING = 2
SLASHING = 3
RADIATION = 4

DMGTYPES = {
    "fire": FIRE,
    "cold": COLD,
    "radiation": RADIATION,
    "bludgeoning": BLUDGEONING,
    "slashing": SLASHING
}

DMGTYPES_REVERSED = {v: k for k, v in DMGTYPES.iteritems()}


class StalledCombatException(Exception):
    pass


class BattleGroup(object):
    def __init__(self, num_units, hp, weaknesses, immunities, attack, dmg_type, init, id):
        self.num_units = num_units
        self.hp = hp
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.attack = attack
        self.dmg_type = dmg_type
        self.init = init
        self.id = id
        self.current_target = None

    @property
    def effective_power(self):
        return self.num_units * self.attack

    @property
    def selection_priority(self):
        return self.effective_power, self.init

    def target_order(self, dmg_type, incoming_damage):
        return self.damage_would_take(dmg_type, incoming_damage), self.effective_power, self.init

    def damage_would_take(self, dmg_type, amount):
        if dmg_type in self.immunities:
            return 0
        elif dmg_type in self.weaknesses:
            return amount * 2
        else:
            return amount

    def deal_damage(self, debug=False):
        if self.current_target:
            total_damage = self.current_target.damage_would_take(self.dmg_type, self.effective_power)
            units_to_kill = min(total_damage // self.current_target.hp, self.current_target.num_units)
            self.current_target.num_units -= units_to_kill
            if debug:
                print("%s attacks %s, killing %d units" % (self.id, self.current_target.id, units_to_kill))
            self.current_target = None
        else:
            if debug:
                print("%s has no current target, cannot deal damage" % self.id)

    def __repr__(self):
        if self.weaknesses:
            weak_str = " weak="
            weak_str += ",".join([DMGTYPES_REVERSED[x] for x in self.weaknesses])
        else:
            weak_str = ''
        if self.immunities:
            immunity_str = " immune="
            immunity_str += " ".join([DMGTYPES_REVERSED[x] for x in self.immunities])
        else:
            immunity_str = ''
        return "BattleGroup[%s](power=%d init=%d num_units=%d hp=%d atk=%d dmg_type=%s%s%s" % (
            self.id,
            self.effective_power,
            self.init,
            self.num_units,
            self.hp,
            self.attack,
            DMGTYPES_REVERSED[self.dmg_type],
            weak_str,
            immunity_str
        )


def parse_line(line, id, boost=0):
    match = MAIN_REGEX.match(line)
    line_dict = match.groupdict()
    immunities, weaknesses = [], []
    if line_dict['modifiers']:
        modifiers = line_dict['modifiers'].split("; ")
        for group in modifiers:
            match = WEAKNESS_REGEX.match(group)
            assert(match is not None)
            modifiers_dict = match.groupdict()
            if modifiers_dict['modifier_type'] == 'immune':
                immunities.extend([DMGTYPES[x] for x in modifiers_dict['dmg_type_list'].split(", ")])
            elif modifiers_dict['modifier_type'] == 'weak':
                weaknesses.extend([DMGTYPES[x] for x in modifiers_dict['dmg_type_list'].split(", ")])

    entity = BattleGroup(id=id, num_units=int(line_dict['num_units']), hp=int(line_dict['hp']),
                         weaknesses=weaknesses, immunities=immunities, attack=int(line_dict['atk'])+boost,
                         dmg_type=DMGTYPES[line_dict['dmg_type']], init=int(line_dict['init']))
    return entity


def parse_input(immune_lines, infection_lines, boost=0):
    immune_list = []
    for i, line in enumerate(immune_lines):
        id = "Immune {}".format(i+1)
        immune_list.append(parse_line(line, id=id, boost=boost))

    infection_list = []
    for i, line in enumerate(infection_lines):
        id = "Infection {}".format(i+1)
        infection_list.append(parse_line(line, id=id))

    return immune_list, infection_list


def select_targets(immune, infection):
    sorted_immune = sorted(immune, key=lambda x: x.selection_priority, reverse=True)
    sorted_infection = sorted(infection, key=lambda x: x.selection_priority, reverse=True)
    chosen_groups = set()
    for bgroup in sorted_immune:
        # Annoyingly, the "skip over immune" proviso is, as far as I can tell, completely absent from the instructions.
        #
        # The instructions say "The attacking group chooses to target the group in the enemy army to which it would
        #   deal the most damage (after accounting for weaknesses and immunities)", which I can only read to mean
        #   "If there's only one enemy and it's immune to the damage type of the first group to choose a target,
        #   the enemy gets picked anyways and the simulation is stalled."
        #
        # My initial (part one) input stalls in this fashion, but I got the correct answer once I removed immune
        #   enemies from target consideration.
        remaining_enemies = [x for x in sorted_infection
                             if x not in chosen_groups and bgroup.dmg_type not in x.immunities]
        if remaining_enemies:
            max_damage_enemy = max(remaining_enemies,
                                   key=lambda x: x.target_order(bgroup.dmg_type, bgroup.effective_power))
            bgroup.current_target = max_damage_enemy
            chosen_groups.add(max_damage_enemy)

    for bgroup in sorted_infection:
        remaining_enemies = [x for x in sorted_immune
                             if x not in chosen_groups and bgroup.dmg_type not in x.immunities]
        if remaining_enemies:
            max_damage_enemy = max(remaining_enemies,
                                   key=lambda x: x.target_order(bgroup.dmg_type, bgroup.effective_power))
            bgroup.current_target = max_damage_enemy
            chosen_groups.add(max_damage_enemy)


def run_attacks(immune, infection, debug=False):
    combined_list = sorted(immune+infection, key=lambda x: x.init, reverse=True)
    for bgroup in combined_list:
        if bgroup.num_units <= 0:
            continue
        else:
            bgroup.deal_damage(debug=debug)
            bgroup.current_target = None

    new_immune = [x for x in immune if x.num_units > 0]
    new_infection = [x for x in infection if x.num_units > 0]
    return new_immune, new_infection


def run_simulation(immune_str, infection_str, boost=0, debug=False):
    immune, infection = parse_input(immune_str, infection_str, boost)
    while len(immune) != 0 and len(infection) != 0:
        if debug:
            print("")
            print("Immune: %r" % ["%s with %d units" % (x.id, x.num_units) for x in immune])
            print("Infection: %r" % ["%s with %d units" % (x.id, x.num_units) for x in infection])
        select_targets(immune, infection)
        old_combatants = sum(x.num_units for x in immune) + sum(x.num_units for x in infection)
        immune, infection = run_attacks(immune, infection, debug=debug)
        new_combatants = sum(x.num_units for x in immune) + sum(x.num_units for x in infection)
        # Some combats devolve into slap fights where the attack is too weak to actually kill any soldiers.
        # This detects a lack of forward progress and raises so we can increment boost and move on with our lives.
        if old_combatants == new_combatants:
            raise StalledCombatException("Total number of soldiers remained %d after a round" % new_combatants)
    return immune, infection


def part_two(immune_str, infection_str, debug=False):
    # Initialize to dummy values with length of 0
    immune, infection = [], []
    boost = 0
    while len(immune) == 0:
        boost += 1
        if debug:
            print("Trying boost level %d" % boost)
        try:
            immune, infection = run_simulation(immune_str, infection_str, boost, debug=debug)
        except StalledCombatException:
            continue

    return immune, infection, boost


immune, infection = run_simulation(IMMUNE, INFECTION, debug=False)
print("Immune: %s" % "\n".join([x.__repr__() for x in immune]))
print("Infection: %s" % "\n".join([x.__repr__() for x in infection]))
print("Total remaining units: %d\n" % (sum(x.num_units for x in immune) + sum(x.num_units for x in infection)))

immune, infection, boost = part_two(IMMUNE, INFECTION, debug=False)
print("Boost level %d will allow immune system to survive" % boost)
print("Immune: %s" % "\n".join([x.__repr__() for x in immune]))
print("Infection: %s" % "\n".join([x.__repr__() for x in infection]))
print("Total remaining units: %d" % (sum(x.num_units for x in immune) + sum(x.num_units for x in infection)))
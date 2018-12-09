class Node(object):
    def __init__(self, value):
        self.next = None
        self.prev = None
        self.value = value

    def __repr__(self):
        return "Node(%d)" % self.value


class CircularMarbles(object):
    def __init__(self, starting_value):
        self.starting_node = Node(starting_value)
        self.starting_node.next = self.starting_node
        self.starting_node.prev = self.starting_node
        self.current_node = self.starting_node

    def insert(self, node, newnode):
        newnode.prev = node
        newnode.next = node.next
        node.next.prev = newnode
        node.next = newnode

    def remove(self, node):
        assert(node is not self.current_node)
        node.prev.next = node.next
        node.next.prev = node.prev
        node.next = None
        node.prev = None
        return node.value

    def add_marble(self, value):
        newnode = Node(value)
        node_to_insert_after = self.current_node.next
        self.insert(node_to_insert_after, newnode)
        self.current_node = newnode

    def remove_marble(self):
        node_to_remove = self.current_node
        for _ in xrange(7):
            node_to_remove = node_to_remove.prev
        new_current = node_to_remove.next
        removed_value = self.remove(node_to_remove)
        self.current_node = new_current
        return removed_value


def generate_scores(num_players, last_marble):
    circle = CircularMarbles(starting_value=0)
    current_marble_value = 1
    player_scores = [0] * num_players
    current_player = 0
    while current_marble_value <= last_marble:
        if current_marble_value % 23 == 0:
            player_scores[current_player] += current_marble_value
            player_scores[current_player] += circle.remove_marble()
        else:
            circle.add_marble(current_marble_value)
        current_marble_value += 1
        current_player = (current_player + 1) % num_players
    return player_scores

print("Max score for 473 players with last marble of 70904 is %d" % max(generate_scores(473, 70904)))
print("Max score for 473 players with last marble of 7090400 is %d" % max(generate_scores(473, 7090400)))

INPUT = open("advent2018_day08_input.txt", "r").read().split(" ")
ALTINPUT = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2".split(" ")

INTINPUT = [int(x) for x in INPUT]


class Node(object):
    def __init__(self, num_children, num_meta):
        self.num_children = num_children
        self.num_meta = num_meta
        self.length = 2
        self.children = []
        self.metadata = []

    def add_child(self, node):
        self.length += node.length
        self.children.append(node)

    def add_meta(self, meta):
        self.length += 1
        self.metadata.append(meta)

    def __repr__(self):
        return "Node(%d children, metadata is %r)" % (self.num_children, self.metadata)


def read_node(inputlist, index=0):
    new_node = Node(num_children=inputlist[index], num_meta=inputlist[index+1])
    index += 2
    for _ in xrange(new_node.num_children):
        child_node = read_node(inputlist, index=index)
        new_node.add_child(child_node)
        index += child_node.length
    for _ in xrange(new_node.num_meta):
        new_node.add_meta(inputlist[index])
        index += 1
    return new_node


def sum_nodes(node):
    current_sum = sum(node.metadata)
    for child in node.children:
        current_sum += sum_nodes(child)
    return current_sum


def sum_nodes_v2(node):
    current_sum = 0
    if node.num_children == 0:
        return sum(node.metadata)
    else:
        for child_num in node.metadata:
            if child_num <= node.num_children and child_num != 0:
                current_sum += sum_nodes_v2(node.children[child_num-1])
    return current_sum


node_tree = read_node(INTINPUT)
print("Sum of metadata: %d" % sum_nodes(node_tree))
print("Child-sum of nodes: %d" % sum_nodes_v2(node_tree))

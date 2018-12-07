INPUT = open("advent2018_day07_input.txt", "r").read().split("\n")
ALTINPUT = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.""".split("\n")


class Node(object):
    def __init__(self, name):
        self.name = name
        self.prereqs = []
        self.unlocks = []

    def add_prereq(self, name):
        self.prereqs.append(name)

    def add_unlock(self, name):
        self.unlocks.append(name)

    def is_available(self, done_so_far):
        if self.name in done_so_far:
            return False
        for node in self.prereqs:
            if node not in done_so_far:
                return False
        return True

    @property
    def time_value(self):
        return ord(self.name[0].upper()) - 64


class Worker(object):
    def __init__(self, time_penalty=0):
        self.time_penalty = time_penalty
        self.current_task = None
        self.current_progress = 0

    def tick(self):
        if self.current_task:
            if self.current_progress < (self.time_penalty + self.current_task.time_value):
                self.current_progress += 1
            else:
                print("Tried to tick on completed task %s!" % self.current_task.name)

    def attempt_claim(self, task):
        if not self.current_task:
            self.current_task = task
            return True
        else:
            return False

    @property
    def is_completed(self):
        if self.current_task:
            return self.current_progress == self.time_penalty + self.current_task.time_value
        else:
            return False

    def attempt_finish_task(self):
        if self.is_completed:
            completed_task = self.current_task.name
            self.current_task = None
            self.current_progress = 0
            return completed_task
        else:
            return None

    def __repr__(self):
        name = self.current_task.name if self.current_task else "None"
        return "Worker(Task: %s, Progress: %s)" % (name, self.current_progress)


def generate_dependencies(lines):
    nodes = {}
    for line in lines:
        prereq = line[5]
        unlock = line[36]
        if prereq not in nodes.keys():
            nodes[prereq] = Node(prereq)
        if unlock not in nodes.keys():
            nodes[unlock] = Node(unlock)
        nodes[prereq].add_unlock(unlock)
        nodes[unlock].add_prereq(prereq)
    return nodes


def available_tasks(dependencies, done_so_far):
    return sorted([key for key, value in dependencies.iteritems() if value.is_available(done_so_far)])

# dependencies = generate_dependencies(ALTINPUT)
# num_workers = 2
# time_penalty = 0
dependencies = generate_dependencies(INPUT)
num_workers = 5
time_penalty = 60
completed = []

while len(completed) < len(dependencies):
    available = available_tasks(dependencies, completed)
    completed.append(available[0])

print("Order of steps: %s" % "".join(completed))

workers = [Worker(time_penalty) for x in range(num_workers)]
completed = []
current_time = 0
available = available_tasks(dependencies, completed)
in_progress = set()
while len(completed) < len(dependencies):
    for task_name in available:
        for worker in workers:
            if task_name not in in_progress and worker.attempt_claim(dependencies[task_name]):
                in_progress.add(task_name)
                break

    for worker in workers:
        worker.tick()
        finished = worker.attempt_finish_task()
        if finished:
            completed.append(finished)
            # print("Completed %s at time %s" % (finished, current_time))
            in_progress.remove(finished)
            available = available_tasks(dependencies, completed)
    current_time += 1

print("Time to completion: %d" % current_time)

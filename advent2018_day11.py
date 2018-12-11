import numpy as np

INPUT = 5153


def calc_power(x, y):
    rack_id = x + 10
    current_power = rack_id * y
    current_power += INPUT
    current_power *= rack_id
    current_power = int(("%03d" % current_power)[-3])
    current_power -= 5
    return current_power


def chunk_array(array, x_size, y_size):
    x_max, y_max = array.shape
    assert(x_max >= x_size)
    assert(y_max >= y_size)
    for i in xrange(0, (x_max-x_size)+1):
        for j in xrange(0, (y_max-y_size)+1):
            yield array[i:i+x_size, j:j+y_size], i, j

calc_power_vector = np.vectorize(calc_power)
grid = np.fromfunction(calc_power_vector, (300, 300))

highest_value = 0
highest_coords = None
for chunk, x, y in chunk_array(grid, 3, 3):
    value = np.sum(chunk)
    if value > highest_value:
        highest_value = value
        highest_coords = (x, y)

print("Highest value for 3x3 is %d" % highest_value)
x, y = highest_coords
print("Highest coords for 3x3 are %d, %d" % (x, y))

highest_value = 0
highest_coords = None
highest_chunk_size = None
for i in xrange(1, 301):
    if i % 10 == 0:
        print("Checking chunks of size %dx%d" % (i, i))
    for chunk, x, y in chunk_array(grid, i, i):
        value = np.sum(chunk)
        if value > highest_value:
            highest_value = value
            highest_coords = (x, y)
            highest_chunk_size = i
            print("Highest value is %d" % highest_value)
            print("Highest coords are %d, %d, %d" % (x, y, i))

print("Highest value is %d" % highest_value)
x, y = highest_coords
print("Highest coords are %d, %d, %d" % (x, y, highest_chunk_size))



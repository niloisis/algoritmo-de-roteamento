file = open('input-tests/input-02', 'r')
line = file.readline()

origin = []
coordinates = {}

row_counter = 0
for line in file:
    column_counter = 0
    for char in line:
        if char == '0':
            column_counter += 1
        elif char == 'R':
            origin = [row_counter, column_counter]
            column_counter += 1
        elif char != '\n' and char != ' ':
            coordinates[char] = [row_counter, column_counter]
            column_counter += 1
    row_counter += 1

file.close()

print(coordinates)
print(origin)


def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def route_distance(lst):
    route = manhattan_distance(origin[1], origin[0], coordinates[lst[0]][1], coordinates[lst[0]][0])
    for i in range(0, len(lst) - 1):
        y1 = coordinates[lst[i]][0]
        x1 = coordinates[lst[i]][1]
        y2 = coordinates[lst[i + 1]][0]
        x2 = coordinates[lst[i + 1]][1]
        route += manhattan_distance(x1, y1, x2, y2)
    route += manhattan_distance(origin[1], origin[0], coordinates[lst[len(lst) - 1]][1],
                                coordinates[lst[len(lst) - 1]][0])
    return route


def permute(str, l):
    if l == len(str):
        min_cost = route_distance(str)
        if min_cost < min_route[0]:
            min_route[0] = min_cost
            min_route[1] = str.copy()
    else:
        for j in range(l, len(str)):
            exchange(str, l, j)
            permute(str, l + 1)
            exchange(str, j, l)


def exchange(str, n, m):
    aux = str[n]
    str[n] = str[m]
    str[m] = aux


delivery_points = list(coordinates.keys())
min_route = [route_distance(delivery_points), ' ']

permute(delivery_points, 0)

print(' '.join(min_route[1]))

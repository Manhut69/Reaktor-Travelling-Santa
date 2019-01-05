import matplotlib.pyplot as plt
import numpy
import math
from random import randrange, shuffle
from copy import deepcopy

MAX_WEIGHT = 10000000
SANTA_HOUSE = [29.315278, 68.073611]


def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6378

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = round(radius * c * 1000)
    return d


def distance_from_trip(start_finish, trip):
    trip_distance = 0
    for child in range(len(trip)):
        if child == 0 or child == len(trip) - 1:
            trip_distance += distance(start_finish, trip[child][1:3])
        else:
            trip_distance += distance(trip[child][1:3], trip[child + 1][1:3])
    return trip_distance


def distance_from_trip_list(start_finish, trip_list):
    total_distance = 0
    for trip in trip_list:
        total_distance += distance_from_trip(start_finish, trip)
    return total_distance


def greedy_fillup(max_weight, id_coordinates_weight_list):
    trip_list = [[]]
    for child in id_coordinates_weight_list:
        child_in_trip = False
        for trip in range(len(trip_list)):
            if sum([i[3] for i in trip_list[trip]]) + child[3] < max_weight:
                trip_list[trip].append(child)
                child_in_trip = True
                break
        if not child_in_trip:
            trip_list.append([child])
    return trip_list


def hillclimb_swap(max_weight, trip_list):
    trip1 = trip_list[randrange(len(trip_list))]
    trip2 = trip_list[randrange(len(trip_list))]
    trip1_dummy = deepcopy(trip1)
    trip2_dummy = deepcopy(trip2)
    child1_index = randrange(len(trip1))
    child2_index = randrange(len(trip2))
    trip1_dummy[child1_index], \
        trip2_dummy[child2_index] = trip2_dummy[child2_index], \
        trip1_dummy[child1_index]
    # print(f"I switched {child1_index} and {child2_index}")
    # print(f"trip 1 is: {[i[0] for i in trip1]}")
    # print(f"dummy trip 1 is: {[i[0] for i in trip1_dummy]}")
    # print(f"trip 2 is: {[i[0] for i in trip2]}")
    # print(f"dummy trip 2 is: {[i[0] for i in trip2_dummy]}")
    if sum([i[3] for i in trip1_dummy]) < max_weight:
        # print("Trip 1 works")
        if sum([i[3] for i in trip2_dummy]) < max_weight:
            # print("Trip 2 works")
            original_distance = distance_from_trip(SANTA_HOUSE, trip1) +\
                distance_from_trip(SANTA_HOUSE, trip2)
            new_distance = distance_from_trip(SANTA_HOUSE, trip1) +\
                distance_from_trip(SANTA_HOUSE, trip2)
            # print(f"Original distance = {original_distance}")
            # print(f"The new distance  = {new_distance}")
            if original_distance > new_distance:
                writefile = open("hillclimblog.txt", 'a')
                trip_list[trip_list.index(trip1)] = trip1_dummy
                trip_list[trip_list.index(trip2)] = trip2_dummy
                total_distance = 0
                for trip in trip_list:
                    trip_distance = 0
                    for child in range(len(trip)):
                        if child == 0 or child == len(trip) - 1:
                            trip_distance += distance(SANTA_HOUSE,
                                                      trip[child][1:3])
                        else:
                            trip_distance += distance(trip[child][1:3],
                                                      trip[child + 1][1:3])
                    total_distance += trip_distance
                writefile.write(f"{total_distance}\n")
    # print(f"\n\n")
    return trip_list


def hillclimb_search(max_weight, trip_list):
    shuffled_trip_list = trip_list      # Maybe deepcopy()?
    shuffle(shuffled_trip_list)
    pick_trip_index = randrange(len(shuffled_trip_list))
    pick_trip = shuffled_trip_list[pick_trip_index]
    pick_child_index = randrange(len(pick_trip))
    for trip in range(len(shuffled_trip_list)):
        this_trip_indexes = [i for i in range(len(shuffled_trip_list[trip]))]
        shuffle(this_trip_indexes)
        original_distance = distance_from_trip(SANTA_HOUSE, pick_trip) +\
            distance_from_trip(SANTA_HOUSE, shuffled_trip_list[trip])
        for child_index in this_trip_indexes:
            shuffled_trip_list[trip][child_index], shuffled_trip_list[pick_trip_index][pick_child_index] = shuffled_trip_list[pick_trip_index][pick_child_index], shuffled_trip_list[trip][child_index]
            if sum([i[3] for i in shuffled_trip_list[trip]]) < max_weight and sum([i[3] for i in shuffled_trip_list[pick_trip_index]]) < max_weight:
                new_distance = distance_from_trip(SANTA_HOUSE, pick_trip) +\
                    distance_from_trip(SANTA_HOUSE, shuffled_trip_list[trip])
                if new_distance < original_distance:
                    return trip_list
                else:
                    shuffled_trip_list[trip][child_index], shuffled_trip_list[pick_trip_index][pick_child_index] = shuffled_trip_list[pick_trip_index][pick_child_index], shuffled_trip_list[trip][child_index]
            else:
                shuffled_trip_list[trip][child_index], shuffled_trip_list[pick_trip_index][pick_child_index] = shuffled_trip_list[pick_trip_index][pick_child_index], shuffled_trip_list[trip][child_index]

    return trip_list


def hillclimb(generations, iterations, max_weight, trip_list):
    writefile = open("hillclimblog.txt", 'w')
    writefile.write(f"{generations} generations\n")
    for generation in range(generations):
        new_trip_list = deepcopy(trip_list)
        writefile.write(f"{distance_from_trip_list(SANTA_HOUSE, new_trip_list)};")
        for i in range(iterations):
            new_trip_list = hillclimb_search(max_weight, new_trip_list)
            writefile.write(f"{distance_from_trip_list(SANTA_HOUSE, new_trip_list)};")
        writefile.write(f"\n")
    return new_trip_list


if __name__ == '__main__':
    nice_list = open("nicelist.txt", "r")
    full_nice_list = []
    distancelist = []
    generations = 4
    iterations = 5000000
    for line in nice_list:
        addlist = []
        child = line.split(";")
        for i in child:
            if "." in i:
                addlist.append(float(i))
            else:
                addlist.append(int(i))
        full_nice_list.append(addlist)
    iterating_list = greedy_fillup(MAX_WEIGHT, full_nice_list)
    iterating_list = hillclimb(generations, iterations, MAX_WEIGHT, iterating_list)
    print("joe")

    readfile = open("hillclimblog.txt", 'r')
    for line in readfile.readlines()[1:]:
        cost_list = line.split(";")[:-1]
        for i in range(len(cost_list)):
            cost_list[i] = int(cost_list[i])
        plt.plot(range(iterations + 1), cost_list)
    plt.show()

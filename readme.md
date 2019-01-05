# travelling santa

https://traveling-santa.reaktor.com/

in nicelist.txt, the following is specified: The child id, the coordinates on earth, the weight of the present in grams

Santa can only have 10.000kg or 10.000.000 grams every trip, and has to start (and end) at 68.073611N 29.315278E every trip

The minimum amount of trips Santa has to make is 531

The following algorithms are applied:

# greedy fill up:

The algorithm picks the trips from the nice list, attempts to put it in the first trip, with the only constraint being the maximum weight.

If it cannot add the child to the current trip, it attempts to add it to the next trip, or, if the current trip was the last trip, it creates a new trip.


# hillclimb:

A 'swap' hillclimber: The algorithm will pick a random child from a random trip, and then compares it with a random child from a random trip, checking the km's travelled, and the weight constraint.

If there's less distance travelled and both the trips have met the weight constraint met, the children are swapped.


A 'search' hillclimber: This script picks a random child, shuffles the trip list, and goes through the trips in random order. If a suitable trip is found (less distance travelled and weight constraint met), it swaps the trips.

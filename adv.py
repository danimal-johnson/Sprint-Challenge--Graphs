from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

# Our map for navigating the world
nav_graph = {}


def reverse_dir(dir):
    """
    Takes a compass direction 'n', 's', 'e', 'w'
    and returns its ordinal opposite direction.
    """
    if dir == 'n':
        return 's'
    if dir == 's':
        return 'n'
    if dir == 'w':
        return 'e'
    if dir == 'e':
        return 'w'


def explore(player, from_room=None, from_dir=None):
    room_id = player.current_room.id
    exits = player.current_room.get_exits()

    # Are we in a new room?
    if room_id not in nav_graph:
        nav_graph[room_id] = {}
        print("New room #", room_id)
        for direction in exits:
            nav_graph[room_id].update({direction: '?'})

    # Where did we come from? Mark it in the nav_graph.
    if from_room != None:
        nav_graph[room_id].update({from_dir: from_room})
        # Don't forget to update the previous room:
        nav_graph[from_room].update({reverse_dir(from_dir): room_id})

    # print(nav_graph)

    print("Room id = ", player.current_room.id)
    print("Options = ", player.current_room.get_exits())
    if 'n' in player.current_room.get_exits():
        print("We can go North!")
        # Now actually go North...
        player.travel('n')
        traversal_path.append('n')
        explore(player, room_id, reverse_dir('n'))

    # End of the line
    return

    # player.travel('n')
    # traversal_path.append('n')
    # print("Room id = ", player.current_room.id)
    # print("Options = ", player.current_room.get_exits())
    # if 'n' in player.current_room.get_exits():
    #     print("Yes!")


# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

explore(player)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")

from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

# Our map for navigating the world
nav_graph = {}
nav_visited = set()


def reverse_dir(dir):
    """
    Takes a compass direction 'n', 's', 'e', 'w'
    and returns its ordinal opposite direction.
    (Helper function.)
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
    """
    Main auto-play navigation function. Recursive.
    Does a DFT of entire maze until all rooms have been visited.
    """
    room_id = player.current_room.id
    exits = player.current_room.get_exits()

    # Are we in a new room?
    if room_id not in nav_graph:
        nav_visited.add(room_id)
        nav_graph[room_id] = {}
        for direction in exits:
            nav_graph[room_id].update({direction: '?'})

    # Where did we come from? Mark it in the nav_graph.
    if from_room != None:
        nav_graph[room_id].update({from_dir: from_room})
        # Don't forget to update the previous room:
        nav_graph[from_room].update({reverse_dir(from_dir): room_id})

    if len(nav_graph) == len(room_graph):
        # All rooms successfully visited!
        return

    # print("Room ", room_id, " = ", nav_graph[room_id])

    # TODO: Loop Optimization
    # TODO: Make code DRY

    # Start by going North, if possible
    # if 'n' in player.current_room.get_exits():
    if nav_graph[room_id].get('n') == '?':
        player.travel('n')
        traversal_path.append('n')
        explore(player, room_id, reverse_dir('n'))

    # When we can't go North anymore, try West next.
    if nav_graph[room_id].get('w') == '?':
        player.travel('w')
        traversal_path.append('w')
        explore(player, room_id, reverse_dir('w'))

    if len(nav_graph) == len(room_graph):
        return

    # When we can't go West anymore, try South.
    if nav_graph[room_id].get('s') == '?':
        player.travel('s')
        traversal_path.append('s')
        explore(player, room_id, reverse_dir('s'))

    if len(nav_graph) == len(room_graph):
        return

    # Finally, try East.
    if nav_graph[room_id].get('e') == '?':
        player.travel('e')
        traversal_path.append('e')
        explore(player, room_id, reverse_dir('e'))

    if len(nav_graph) == len(room_graph):
        return

    # All options have been exhausted. Head back...
    if from_dir != None:
        player.travel(from_dir)
        # Don't forget to record our trip back!
        traversal_path.append(from_dir)

    return


# Fill this out with directions to walk
traversal_path = []

# Auto-play (find all nodes of the maze)
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

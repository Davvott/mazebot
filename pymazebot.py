"""Davvotts attempt at MazeBot"""
from mazebot.mazeBotClass import RandomMazeBot
DOMAIN = "https://api.noopschallenge.com"
RANDOM = "/mazebot/random"
RACE = "/mazebot/race/start"
AUTH = "Davvott"
PARAMS = {"maxSize":10}

# SOLUTION SAMPLE
sample = {
    "directions": "ESS"
}


def main():
    # Login for race mode only
    maze_bot = RandomMazeBot()
    print(maze_bot)

    continue_maze = True
    solution = []
    while continue_maze:

        # Code here to complete maze
        move = get_player_move()
        maze_bot.move_bot(move)
        solution.append(move)
        print_maze(maze_bot)
        if maze_bot.check_end():
            print("Success!!!!!")
            continue_maze = False

        # try:
        #     result = send_solution(maze_path, directions)
        #     if result['result'] == "success":
        #         maze_path = result['nextMaze']
        #         next_maze = get_json(maze_path)
        # except:
        #     pass


def get_player_move():
    """Basic logic to get user input"""
    wasd = ["W", "S", "A", "D"]
    cardinal = ["N", "S", "W", "E"]
    move = input("\nMove - W, S, A, D: ").upper()
    while move not in wasd:
        print("Try again")
        move = input("Move - W, S, A, D: ").upper()
    print(cardinal[wasd.index(move)])
    return cardinal[wasd.index(move)]


def print_maze(bot):
    """Console print function"""
    bot.map[bot.y][bot.x] = "A"
    print(bot)


main()

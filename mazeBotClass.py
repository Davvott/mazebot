"""Basic Class to handle mazeBot functionality"""
import requests

DOMAIN = "https://api.noopschallenge.com"
RANDOM = "/mazebot/random"
RACE = "/mazebot/race/start"
AUTH = "Davvott"
PARAMS = {"maxSize": 10}


class RandomMazeBot:
    """Initialise Random maze. position, and other data"""

    def __init__(self):
        start_random = requests.get(DOMAIN + RANDOM, params=PARAMS)
        random_maze = start_random.json()
        self.name = random_maze['name']
        self.maze_path = random_maze['mazePath']
        self.map = random_maze['map']
        self.cols = len(self.map[0])
        self.rows = len(self.map)
        self.x, self.y = random_maze["startingPosition"]  # [x, y]
        self.end_pos = random_maze["endingPosition"]

    def __str__(self):
        maze_map = "\n".join(" ".join(l) for l in self.map)
        return "Name: {}, Start: {}, End: {}, Map:\n{}".format(self.name, self.pos, self.end_pos, maze_map)

    def move_bot(self, direction):
        """Uses Cardinal Directions to move position, returns True/False"""
        directions = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}
        # set current pos on map to ".",
        self.map[self.y][self.x] = "."
        x, y = directions[direction]

        if self.check_move(x, y):
            # Update self position
            self.x += x
            self.y += y
            return True
        else:
            return False

    def check_move(self, x, y):
        """Check potential move"""
        return self.map[self.y+y][self.x+x] == " "

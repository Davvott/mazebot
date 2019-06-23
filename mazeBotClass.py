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
        self.x, self.y = random_maze["startingPosition"]
        self.end_pos = random_maze["endingPosition"]  # [x, y]
        self.completion = False

    def __str__(self):
        maze_map = "\n".join(" ".join(l) for l in self.map)
        return "Name: {}, Pos: {}, End: {}\nMap:{}\n{}".format(
            self.name, (self.x, self.y), self.end_pos, "- "*self.cols, maze_map)

    def move_bot(self, direction):
        """Uses Cardinal Directions to move position, returns True/False.
        Map North is -1 for list of lists. """
        directions = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
        x, y = directions[direction]
        if self.check_move(x, y):
            # set current pos on map to ".",
            self.map[self.y][self.x] = "."
            # Update self position
            self.x += x
            self.y += y
            return True
        else:
            return False

    def check_move(self, x, y):
        """Check potential move for space or finish"""
        try:
            return self.map[self.y+y][self.x+x] == " " or [self.x+x, self.y+y] == self.end_pos
        except IndexError:
            return False

    def check_end(self):
        """Self check of self.pos == self.end_pos"""
        return [self.x, self.y] == self.end_pos

    def send_challenge_solution(self, solution):
        """To win, or not to win. That is the challenge."""
        post = DOMAIN + self.maze_path
        solution = "".join(s for s in solution)
        print(post)
        req = requests.post(post, json={'directions':solution})
        r = req.json()
        print(r)
        try:
            if r['result'] == 'correct':
                self.completion = True
        except KeyError as error:
            print(error)
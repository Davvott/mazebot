"""Basic Class to handle mazeBot functionality"""
import requests

DOMAIN = "https://api.noopschallenge.com"
RANDOM = "/mazebot/random"
RACE = "/mazebot/race/start"
AUTH = "Davvott"
PARAMS = {"maxSize": 10}


class AutomatedMazeBot:
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
        self.solution = []
        self.junction = {}
        self.completion = False

    def __str__(self):
        maze_map = "\n".join(" ".join(l) for l in self.map)
        return "Name: {}, Pos: {}, End: {}, Map:\n{}".format(
            self.name, (self.x, self.y), self.end_pos, maze_map)

    def check_neighbor_options(self):
        """Checks map for neighbors, returns cardinal directions list"""
        nei = []
        d = ["E", "W", "S", "N"]
        directions = [(1, 0), (0, 1)]
        x, y = self.x, self.y
        deltas = (1, -1)
        count = 0
        for delta_x, delta_y in directions:  # For unpacked tups in list
            for delta in deltas:
                delta_x *= delta
                delta_y *= delta
                next_x = x + delta_x
                next_y = y + delta_y
                # Checks E, W, S, N (1,0) (-1,0) (0,1) (0, -1)

                if 0 <= next_y < self.rows and 0 <= next_x < self.cols:
                    # Special Case
                    if self.map[next_y][next_x] == "B":
                        # NOT SRP but...
                        self.move_bot(d[count])
                        self.check_end()
                        return []  # To break while loop in find path
                    elif self.map[next_y][next_x] == " ":
                        nei.append(d[count])
                count += 1
        return nei

    def move_bot(self, direction):
        """Uses Cardinal Directions to move position in given direction"""
        directions = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}

        x, y = directions[direction]

        if self.map[self.y + y][self.x + x] == ".":
            # Backtracking! Remove last solution item
            self.solution.pop()
            # Reset maze spot and move bot
            self.map[self.y][self.x] = "X"
            self.x += x
            self.y += y
        else:
            # set current pos on map to ".",
            self.map[self.y][self.x] = "."
            # Update self position
            self.x += x
            self.y += y
            self.solution.append(direction)

    def find_path(self):
        """ Logic for path finding. Rudimentary, inefficient"""
        nei = self.check_neighbor_options()

        self.check_end()  # At the finish line, no more work to be done

        # Dead End
        if len(nei) == 0:
            self.crossroads(nei)

        # Crossroad
        elif len(nei) > 1:
            self.crossroads(nei)

        else:
            while len(nei) == 1:
                # If only one direction to move, move it!
                self.move_bot(nei[0])
                nei = self.check_neighbor_options()


    def crossroads(self, nei):
        """ Handle junction call """
        # Dead junction
        if len(nei) == 0 and (self.x, self.y) in self.junction:
            del self.junction[self.x, self.y]
            self.backtrack()
        # Dead end
        elif len(nei) == 0:
            self.backtrack()
        # Active Junction
        else:
            self.junction[self.x, self.y] = nei
            print("junction", self.junction)
            direction = nei.pop()
            print("Moving ", direction)
            self.move_bot(direction)

    def backtrack(self):
        """Backtrack to most recent junction"""
        while (self.x, self.y) not in [key for key in self.junction.keys()]:
            reverse_direction = {"N": "S", "S": "N", "E": "W", "W": "E"}
            direction = reverse_direction[self.solution[-1]]
            self.move_bot(direction)  # move_bot pops solution

    def check_end(self):
        """Self check of self.pos == self.end_pos"""
        if [self.x, self.y] == self.end_pos:

            self.completion = True
            self.send_challenge_solution()



    def get_json(self, path):
        print("*** GET {}".format(path))

        response = requests.get(path)
        r = response.json()
        print("HTTP {}".format(r))

        return r

    def send_challenge_solution(self):
        """To win, or not to win. That is the challenge."""
        post = DOMAIN + self.maze_path
        solution = "".join(s for s in self.solution)
        print(post)
        req = requests.post(post, json={'directions': solution})
        r = req.json()
        print(r)
        try:
            if r['result'] == 'correct':
                self.completion = True
        except KeyError as error:
            print(error)


if __name__ == "__main__":
    test_bot = AutomatedMazeBot()
    print(test_bot)

    test_bot.find_path()
    print(test_bot)

    for i in range(100):
        test_bot.find_path()
        if test_bot.completion:
            break
        print(test_bot)

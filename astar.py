from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import *

def key(state):
    """
    Returns a key that uniquely identifies a Pacman game state.

    Arguments:
    ----------
    - `state`: the current game state. See FAQ and class
               `pacman.GameState`.

    Return:
    -------
    - A hashable key object that uniquely identifies a Pacman game state.
    """
    return (state.getPacmanPosition(), state.getFood()) #we changed this 



def heruistic(sum, foodCount):
    if foodCount == 0 :
        return 0
    return sum / foodCount


def getCost(path, nbFoodLeft):
    return  1 + nbFoodLeft + len(path)

def estimatedCost(item):
    foodMatrix = item[0].getFood()
    pacmanPosition = item[0].getPacmanPosition()
    foodCount = 0
    sum = 0

    for i in range(foodMatrix.width):
        for j in range(foodMatrix.height):
            if (foodMatrix[i][j] == True):
                sum += manhattanDistance(pacmanPosition, (i,j))
                foodCount += 1

    return  getCost(item[1],foodCount) + heruistic(sum,foodCount)




class PacmanAgent(Agent):
    """
    A Pacman agent based on Depth-First-Search.
    """

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.moves = []

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """

        if not self.moves:
            self.moves = self.astar(state)

        try:
            return self.moves.pop(0)

        except IndexError:
            return Directions.STOP



    def astar(self, state):
        """
        Given a pacman game state,
        returns a list of legal moves to solve the search layout.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A list of legal moves as defined in `game.Directions`.
        """
        path = []
        fringe = PriorityQueueWithFunction(estimatedCost)
        fringe.push((state, path)) 
        closed = set()

        while True:
            if fringe.isEmpty() == True:
                print("Failure")
                return []  # failure

            current, path = fringe.pop()[1]

            if current.isWin():
                return path

            current_key = key(current)

            if current_key not in closed:
                closed.add(current_key)

                for next_state, action in current.generatePacmanSuccessors():
                    fringe.push((next_state, path + [action]))

        return path

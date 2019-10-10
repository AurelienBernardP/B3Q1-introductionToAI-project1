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
    return (state.getPacmanPosition(), state.getFood())



def heuristic(sumManhattanDist, nbFood):
    """
    Returns the forward cost given parameters of a Pacman game state

    Arguments:
    ----------
    - `sumManhattanDist`: the sum of each manhattan distance between the
                          position of Pacman and the remaining food.
    - `nbFood`: the remaining number of food

    Return:
    -------
    - A real that represents the forward cost of the given Pacman game state.
    """
    if nbFood == 0 :
        return 0

    return sumManhattanDist / nbFood


def backwardCost(path, nbFood):
    """
    Returns the backward cost given parameters of a Pacman game state

    Arguments:
    ----------
    - `path`: the path taken by Pacman
    - `nbFood`: the remaining number of food

    Return:
    -------
    - A non-nul integer that represents the backward cost of the given Pacman game state.
    """
    return  1 + nbFoodLeft + len(path)

def optimalCost(item):
    """
    Returns the estimated cost of the cheapest solution given a Pacman game 
    state and the taken path to reach that state.

    Arguments:
    ----------
    - `item`: A tuple of a Pacman game state and the taken path to reach that state

    Return:
    -------
    - A non-zero real number that represents the optimal cost to reach the goal state.
    """

    state = item[0]
    path = item[1]

    foodMatrix = state.getFood()
    pacmanPosition = state.getPacmanPosition()
    nbFood = 0
    sumManhattanDist = 0

    #Going through the matrix to count the remaining food in the game
    for i in range(foodMatrix.width):
        for j in range(foodMatrix.height):
            if (foodMatrix[i][j] == True):
                sumManhattanDist += manhattanDistance(pacmanPosition, (i,j))
                nbFood += 1

    return  backwardCost(path,nbFood) + heuristic(sumManhattanDist,nbFood)




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
        closed = set()
        fringe = PriorityQueueWithFunction(optimalCost)
        fringe.push((state, path))

        while True:
            if fringe.isEmpty() == True:
                print("Failure")
                return [] 

            current, path = fringe.pop()[1]

            if current.isWin():
                return path

            current_key = key(current)

            if current_key not in closed:
                closed.add(current_key)
                for next_state, action in current.generatePacmanSuccessors():
                    fringe.push((next_state, path + [action]))

        return path

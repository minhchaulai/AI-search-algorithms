# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # obviously we bias Pac to immediately win if possible, and avoid losing
        if successorGameState.isWin():
            return float("inf")
        if successorGameState.isLose():
            return float("-inf")

        # We want to find the position of every ghost, and if the ghost is within two manhattan distances, we want to encourage Pac to avoid them (obviously)
        for ghostState in newGhostStates:
            ghostPosition = ghostState.getPosition()
            pacGhostDist = manhattanDistance(ghostPosition, newPos)
            if pacGhostDist < 2:
                return float("-inf")

        # The only condition left to consider is food
        # we compile a list of distances to each food left in the game
        # If there's food left, then we encourage Pac to go after it by taking the inverse
        foods = []
        for food in newFood.asList():
            foods.append(manhattanDistance(newPos, food))
        minFood = min(foods)
        invMin = 0
        if len(foods) > 0 and minFood > 0:
            invMin = 1 / minFood
        return invMin + successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)



class MinimaxAgent(MultiAgentSearchAgent):
    """
        Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
            Returns the minimax action from the current gameState using self.depth
            and self.evaluationFunction.

            Here are some method calls that might be useful when implementing minimax.

            gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

            gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

            gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()

        def pacMax(gameState, depth, returnMove=False):
            # if we reach terminating node, simply return heuristic value of node
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)

            value = float("-inf")
            move = Directions.STOP

            for action in gameState.getLegalActions():
                nextAction = minGhost(gameState.generateSuccessor(0, action), depth)
                if nextAction > value:
                    value = nextAction
                    move = action
            return move if returnMove else value

        def minGhost(gameState, depth, agent=1):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)

            value = float("inf")

            if agent == numAgents - 1:
                for action in gameState.getLegalActions(agent):
                    value = min(value, pacMax(gameState.generateSuccessor(agent, action), depth - 1))

            else:
                for action in gameState.getLegalActions(agent):
                    value = min(value, minGhost(gameState.generateSuccessor(agent, action), depth, agent + 1))
            return value

        return pacMax(gameState, self.depth, True)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
        Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # alpha beta is the same as our minimax, but we add in alpha beta in
        # order to prune the tree and avoid expanding paths we don't need
        # we continually adjust alpha and beta to make our bounds tight
        numAgents = gameState.getNumAgents()

        def pacMax(gameState, depth, alpha, beta, returnMove=False):
            # if we reach terminating node, simply return heuristic value of node
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)

            value = float("-inf")
            move = Directions.STOP

            for action in gameState.getLegalActions():
                nextAction = minGhost(gameState.generateSuccessor(0, action), depth, alpha, beta)
                if nextAction > value:
                    value = nextAction
                    move = action
                if value > beta:
                    return move if returnMove else value
                alpha = max(alpha, value)
            return move if returnMove else value

        def minGhost(gameState, depth, alpha, beta, agent=1):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)

            value = float("inf")

            if agent == numAgents - 1:
                for action in gameState.getLegalActions(agent):
                    value = min(value, pacMax(gameState.generateSuccessor(agent, action), depth - 1, alpha, beta))
                    if value < alpha:
                        return value
                    beta = min(beta, value)
            else:
                for action in gameState.getLegalActions(agent):
                    value = min(value, minGhost(gameState.generateSuccessor(agent, action), depth, alpha, beta, agent + 1))
                    if value < alpha:
                        return value
                    beta = min(beta, value)
            return value

        return pacMax(gameState, self.depth, float("-inf"), float("inf"), True)



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()

        def pacMax(gameState, depth, returnMove=False):
            # if we reach terminating node, simply return heuristic value of node
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)

            value = float("-inf")
            move = Directions.STOP

            for action in gameState.getLegalActions():
                nextAction = minGhost(gameState.generateSuccessor(0, action), depth)
                if nextAction > value:
                    value = nextAction
                    move = action
            return move if returnMove else value

        def minGhost(gameState, depth, agent=1):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)

            value = 0
            numMoves = 0

            if agent == numAgents - 1:
                for action in gameState.getLegalActions(agent):
                    value += pacMax(gameState.generateSuccessor(agent, action), depth - 1)
                    numMoves += 1
            else:
                for action in gameState.getLegalActions(agent):
                    value += minGhost(gameState.generateSuccessor(agent, action), depth, agent + 1)
                    numMoves += 1
            return value/numMoves

        return pacMax(gameState, self.depth, True)


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: For this better evaluation function, we're evaluating the states and using the following features linearly combined together: the distance to food, the distance to ghosts, the distance to scared ghosts, the amount of food left on the board, and the amount of pellets left on the board, weighted in that order.
    """
    "*** YOUR CODE HERE ***"
    # as before, we want to win and avoid losing
    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return float("-inf")

    # get current state of game
    pacmanPos = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates()
    foodPos = currentGameState.getFood()
    capsules = currentGameState.getCapsules()

    # find distance to closest food
    foodDist = [(manhattanDistance(pacmanPos, food)) for food in foodPos.asList()]
    minFoodDist = min(foodDist)

    # find distances to closest ghost and scared ghost, if it exists
    GhostDist = [manhattanDistance(pacmanPos, ghostState.getPosition()) for ghostState in ghostStates if ghostState.scaredTimer == 0]
    minGhostDist = -3
    if len(GhostDist) > 0:
        minGhostDist = min(GhostDist)
    scaredGhostDist = [manhattanDistance(pacmanPos, ghostState.getPosition()) for ghostState in ghostStates if ghostState.scaredTimer > 0]
    minScaredGhostDist = 0
    if len(scaredGhostDist) > 0:
        minScaredGhostDist = min(scaredGhostDist)

    # now that we've generated the features of the states we're examining
    # add features linearly, encouraging Pac to go for pellets, reduce the
    # the amount of food in the state, eat food and ghosts, and avoid ghosts otherwise
    score = scoreEvaluationFunction(currentGameState)
    #
    score += -2 * minFoodDist
    score += -3 * (1.0 / minGhostDist)
    score += -4 * minScaredGhostDist
    score += -25 * len(capsules)
    score += -10 * len(foodPos.asList())

    return score




# Abbreviation
better = betterEvaluationFunction

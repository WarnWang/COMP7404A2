# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

import random
import sys

import util
from game import Agent, Directions


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
        legal_moves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = random.choice(best_indices)  # Pick randomly among the best

        "Add more of your code here if you want to"
        return legal_moves[chosen_index]

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
        successor_game_state = currentGameState.generatePacmanSuccessor(action)
        new_pos = successor_game_state.getPacmanPosition()
        new_food = successor_game_state.getFood()
        new_ghost = successor_game_state.getGhostStates()
        ghost_pos = successor_game_state.getGhostPositions()

        "*** YOUR CODE HERE ***"
        # If this is win state, return the maximum value
        if successor_game_state.isWin():
            return sys.maxint

        # Hold negative position on stop, encourage agent to take other actions
        if action == Directions.STOP:
            next_score = 0
        else:
            next_score = 1

        # Calculate the ghost related score
        for i in range(len(ghost_pos)):
            distance = util.manhattanDistance(new_pos, ghost_pos[i])

            # which means ghost is eatable
            if new_ghost[i].scaredTimer > 0:
                next_score += new_ghost[i].scaredTimer - distance
            else:

                # This position is very dangerous, so use the minimal value to represent
                if distance < 2:
                    return -sys.maxint

                # encourage the agent keep away from ghost, regard distance larger than 5 as safe
                elif distance > 5:
                    next_score += 5
                else:
                    next_score += distance

        # Calculate the food impact
        food_list = new_food.asList()
        next_pos = new_pos

        # If new position has a food, add 10 score
        if currentGameState.getFood()[new_pos[0]][new_pos[1]]:
            next_score += 10

        # Else find the nearest food position
        elif food_list:
            length = util.manhattanDistance(food_list[0], next_pos)
            for i in food_list:
                new_length = util.manhattanDistance(i, next_pos)
                if new_length < length:
                    length = new_length
            next_score -= length

        return next_score


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        Agent.__init__(self)
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minmax action from the current gameState using self.depth
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
        possible_next_action_list = gameState.getLegalActions(0)
        max_value = -sys.maxint
        next_action = Directions.STOP
        agent_num = gameState.getNumAgents()
        if agent_num > 1:
            next_agent = 1
            depth = 0
        else:
            next_agent = 0
            depth = 1

        for action in possible_next_action_list:
            next_state = gameState.generateSuccessor(0, action)
            if next_state.isWin():
                return action
            current_value = self.evaluate_actions(next_agent, depth, next_state)
            if current_value > max_value:
                max_value = current_value
                next_action = action
        return next_action

    def evaluate_actions(self, agent_index, depth, gameState):
        agent_num = gameState.getNumAgents()
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        elif agent_index == agent_num - 1:
            depth += 1
            next_agent_index = 0

        else:
            next_agent_index = agent_index + 1

        possible_next_action_list = gameState.getLegalActions(agent_index)
        min_value = sys.maxint
        max_value = -sys.maxint
        for action in possible_next_action_list:
            next_state = gameState.generateSuccessor(agent_index, action)
            if next_state.isWin() or next_state.isLose():
                current_value = self.evaluationFunction(next_state)
            else:
                current_value = self.evaluate_actions(next_agent_index, depth, next_state)
            if current_value > max_value:
                max_value = current_value

            if current_value < min_value:
                min_value = current_value

        if agent_index == 0:
            return max_value
        else:
            return min_value


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


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
        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction


class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

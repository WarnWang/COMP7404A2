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

import util
from game import Agent, Directions

MAX_VALUE = 2 ** 16 - 1
MIN_VALUE = 1 - 2 ** 16

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
            return MAX_VALUE

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
                    return MIN_VALUE

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

        # init some parameter for next steps
        possible_next_action_list = gameState.getLegalActions(0)
        max_value = MIN_VALUE
        next_action = Directions.STOP
        agent_num = gameState.getNumAgents()

        # get next agent index and next depth
        if agent_num > 1:
            next_agent = self.index + 1
            depth = 0
        else:
            next_agent = self.index
            depth = 1

        # Travel all the possible actions to determine the best action
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
        '''
        Evaluation function to calculate the action score
        '''

        # Get the agent number
        agent_num = gameState.getNumAgents()

        # Check whether both Pacman or ghosts moving enough times or current state is a goal state
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        # If all ghosts moved, next moved actor would be Pacman
        elif agent_index == agent_num - 1:
            depth += 1
            next_agent_index = self.index

        # Get next ghost agent index
        else:
            next_agent_index = agent_index + 1

        # Init some values
        possible_next_action_list = gameState.getLegalActions(agent_index)
        min_value = MAX_VALUE
        max_value = MIN_VALUE

        for action in possible_next_action_list:
            next_state = gameState.generateSuccessor(agent_index, action)

            # if next_state is goal state, then there is no need to further evaluate
            if next_state.isWin() or next_state.isLose():
                current_value = self.evaluationFunction(next_state)

            # Recursively calculate the state cost
            else:
                current_value = self.evaluate_actions(next_agent_index, depth, next_state)

            # Update the max and min value
            if current_value > max_value:
                max_value = current_value
            if current_value < min_value:
                min_value = current_value

        # If agent is Pacman, then it need the max_value, otherwise, it will need the min_value
        if agent_index == self.index:
            return max_value
        else:
            return min_value


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        MultiAgentSearchAgent.__init__(self, evalFn, depth)

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # init some parameter for next steps
        possible_next_action_list = gameState.getLegalActions(0)
        max_value = MIN_VALUE
        next_action = Directions.STOP
        agent_num = gameState.getNumAgents()

        # get next agent index and next depth
        if agent_num > 1:
            next_agent = self.index + 1
            depth = 0
        else:
            next_agent = self.index
            depth = 1

        # Travel all the possible actions to determine the best action
        alpha = MIN_VALUE
        beta = MAX_VALUE
        for action in possible_next_action_list:
            next_state = gameState.generateSuccessor(0, action)
            if next_state.isWin():
                return action
            current_value = self.evaluate_actions(next_agent, depth, next_state, alpha, beta)
            if current_value > max_value:
                max_value = current_value
                next_action = action
            alpha = max(alpha, max_value)

        return next_action

    def evaluate_actions(self, agent_index, depth, game_state, alpha, beta):
        '''
        Evaluate the action performance
        :param agent_index: the index of action that need to be evaluated
        :param depth: how many depth has been explored
        :param game_state: Current game state
        :param alpha: Current alpha
        :param beta: Current beta
        :return: The score of current action
        '''

        # Check whether both Pacman or ghosts moving enough times or current state is a goal state
        if depth == self.depth or game_state.isWin() or game_state.isLose():
            return self.evaluationFunction(game_state)

        # Based on the agent type, decide which function should be used
        if agent_index == 0:
            return self.max_value(game_state, depth, alpha, beta)
        else:
            return self.min_value(game_state, depth, agent_index, alpha, beta)

    def max_value(self, game_state, depth, alpha, beta):
        '''
        Function to evaluate the max agent
        :param game_state: current game state
        :param depth: current game depth
        :param alpha: current alpha
        :param beta: current beta
        :return: current score
        '''

        # Get the agent number
        agent_num = game_state.getNumAgents()

        # We can make sure that this state is not the goal state, so Just generate successors directly
        possible_action_list = game_state.getLegalActions(0)

        max_value = MIN_VALUE

        # Determine next agent and depth index
        if agent_num == 1:
            next_agent = 0
            next_depth = depth + 1
        else:
            next_agent = 1
            next_depth = depth

        # Travel all possible states
        for action in possible_action_list:
            next_game_state = game_state.generateSuccessor(0, action)
            if next_game_state.isWin() or next_game_state.isLose():
                current_value = self.evaluationFunction(next_game_state)

            else:
                current_value = self.evaluate_actions(next_agent, next_depth, next_game_state, alpha, beta)

            max_value = max(current_value, max_value)

            # If max value greater than beta, we can prune the following path
            if max_value > beta:
                return max_value

            # Get new alpha
            alpha = max(alpha, max_value)

        return max_value

    def min_value(self, game_state, depth, agent_index, alpha, beta):
        '''
        Function to evaluate the max agent
        :param game_state: current game state
        :param depth: current game depth
        :param alpha: current alpha
        :param beta: current beta
        :param agent_index: The agent that need to be judged
        :return: current score
        '''

        # Get the agent number
        agent_num = game_state.getNumAgents()

        # We can make sure that this state is not the goal state, so Just generate successors directly
        possible_action_list = game_state.getLegalActions(agent_index)

        min_value = MAX_VALUE

        # Determine next agent and depth index
        if agent_num == agent_index + 1:
            next_agent = 0
            next_depth = depth + 1
        else:
            next_agent = agent_index + 1
            next_depth = depth

        # Travel all possible states
        for action in possible_action_list:
            next_game_state = game_state.generateSuccessor(agent_index, action)
            if next_game_state.isWin() or next_game_state.isLose():
                current_value = self.evaluationFunction(next_game_state)

            else:
                current_value = self.evaluate_actions(next_agent, next_depth, next_game_state, alpha, beta)

            min_value = min(current_value, min_value)
            # If max value greater than alpha, we can prune the following path
            if min_value < alpha:
                return min_value

            # get new beta
            beta = min(beta, min_value)

        return min_value


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

        # init some parameter for next steps
        max_value = MIN_VALUE
        next_action = Directions.STOP
        if gameState.isLose() or gameState.isWin():
            return next_action

        possible_next_action_list = gameState.getLegalActions(0)
        agent_num = gameState.getNumAgents()

        # get next agent index and next depth
        if agent_num > 1:
            next_agent = self.index + 1
            depth = 0
        else:
            next_agent = self.index
            depth = 1

        # Travel all the possible actions to determine the best action
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
        '''
        Evaluation function to calculate the action score
        '''

        # Get the agent number
        agent_num = gameState.getNumAgents()

        # Check whether both Pacman or ghosts moving enough times or current state is a goal state
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        # If all ghosts moved, next moved actor would be Pacman
        elif agent_index == agent_num - 1:
            depth += 1
            next_agent_index = self.index

        # Get next ghost agent index
        else:
            next_agent_index = agent_index + 1

        # Init some values
        possible_next_action_list = gameState.getLegalActions(agent_index)
        max_value = MIN_VALUE
        total_value = 0

        for action in possible_next_action_list:
            next_state = gameState.generateSuccessor(agent_index, action)

            # if next_state is goal state, then there is no need to further evaluate
            if next_state.isWin() or next_state.isLose():
                current_value = self.evaluationFunction(next_state)

            # Recursively calculate the state cost
            else:
                current_value = self.evaluate_actions(next_agent_index, depth, next_state)

            # Update the max and total value
            if current_value > max_value:
                max_value = current_value
            total_value += current_value

        # If agent is Pacman, then it need the max_value, otherwise, it will need the average value
        if agent_index == self.index:
            return max_value
        else:
            return total_value / float(len(possible_next_action_list))


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

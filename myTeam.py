# from pacai.util import reflection
from pacai.agents.capture.reflex import CaptureAgent
from pacai.core.distance import manhattan
import random
# from pacai.util import util

# TODO: do not import qulafied import THIS IS ONE OF THE CHECKS KAIA
# IDFK WHAT TO DO I WANNA CRYYYYYY
# TODO: make both agents offensive agents instead of defenisve offensive??
# TODO: implement getAction 
# TODO: implement getCapsule (getFood is a method we have access too)
# TODO: use getScore as a check to see how we're doing in the match; if we're doing really 
# well consider switching to full defense? else stick with offense? 
# would this change the chooseAction function? as in if the score is high it needs to pick 
# an action that is defensive rather than offensive

def createTeam(firstIndex, secondIndex, isRed,
        first = 'pacai.agents.capture.dummy.DummyAgent',
        second = 'pacai.agents.capture.dummy.DummyAgent'):
    """
    This function should return a list of two agents that will form the capture team,
    initialized using firstIndex and secondIndex as their agent indexed.
    isRed is True if the red team is being created,
    and will be False if the blue team is being created.
    """

    # batu said get rid of qualified import
    # firstAgent = reflection.qualifiedImport(first)
    # secondAgent = reflection.qualifiedImport(second)

    return [
        defensiveAgent(firstIndex),
        offensiveAgent(secondIndex),
    ]

# reflex capture agent ???
class defensiveAgent(CaptureAgent):
    def getFeatures(self, gameState, action):
        features = {}
        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)

        # feature 1: score
        features['successorScore'] = self.getScore(successor)

        # feature 2: distance to nearest food
        foodList = self.getFood(successor).asList()
        if len(foodList) > 0:
            myPos = myState.getPosition()
            minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minDistance

        # TODO: add more features here based on strategy
        return features

    def getWeights(self, gameState, action):
        # define weights for features 
        # adjust these values to reflect strategy
        return {
            'successorScore': 100,
            'distanceToFood': -1,
            # TODO: add more feature weights as needed
        }

# reflex capture agent ???
class offensiveAgent(CaptureAgent):
    def getFeatures(self, gameState, action):
        features = {}
        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)

        # feature 1: score (negative to encourage defensive play)
        features['successorScore'] = -self.getScore(successor)

        # feature 2: distance to nearest invader
        opponents = self.getOpponents(successor)
        invaders = [successor.getAgentState(i) for i in opponents if successor.getAgentState(i).isPacman]
        if len(invaders) > 0:
            myPos = myState.getPosition()
            minDistance = min([self.getMazeDistance(myPos, invader.getPosition()) for invader in invaders])
            features['distanceToInvader'] = minDistance
        else:
            features['distanceToInvader'] = 0  # no invaders, no penalty

        # TODO: add more features here based on defensive strategy

        return features

    def getWeights(self, gameState, action):
        # define weights for features
        # adjust these values to reflect defensive strategy
        return {
            'successorScore': -100,
            'distanceToInvader': -1,
            # TODO: add more feature weights as needed
        }
    
    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """
        legalActions = self.getLegalActions(gameState)
        # if there are no legal actions
        if not legalActions:
            return None
        # with probability epsilon, choose a random action
        if flipCoin(self.epsilon):
            return random.choice(legalActions)
        else:
            # otherwise, choose the action with the maximum Q-value
            return self.getPolicy(gameState)
            features['distanceToInvader'] = 0  # no invaders, no penalty

    def getWeights(self, gameState, action):
        # define weights for features
        # adjust these values to reflect defensive strategy
        return {
            'successorScore': -100,
            'distanceToInvader': -1,
            # TODO: add more feature weights as needed
        }
        # collect legal moves.
        legalMoves = gameState.getLegalActions()
        # choose one of the best actions.
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.
        # get action needs to return the best action as pacman
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.
        """
        # Useful information you can extract.
        # newPosition = successorGameState.getPacmanPosition()
        # oldFood = currentGameState.getFood()
        # newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]

        # *** Your Code Here ***
        # generate the successor game state
        # after taking in the action that was specificed
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        # getScaredTime is the time
        newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]

        CapsuleLocations = self.getCapsule(currentGameState)  # capsules on enemy team
        # initialize a score based on the current game state's score
        score = successorGameState.getScore()
        # calculate distances to the closest food pellet
        foodDistances = [manhattan(newPos, food) for food in newFood.asList()]
        if foodDistances:
            closestFoodDistance = min(foodDistances)
            # add a positive score for being closer to the food
            # the reciprocal of the distance is used here???
            score += 1.0 / closestFoodDistance
        # avoid ghosts if they are not scared, and approach them if they are
        for ghost, scaredTime in zip(newGhostStates, newScaredTimes):
            ghostPos = ghost.getPosition()
            # if a ghost is too close, and not scared
            # then aviod it (negative score?)
            if scaredTime == 0 and manhattan(newPos, ghostPos) < 2:
                score -= 1000  # strongly avoid ghosts
            # if a ghost is too close and scared
            # approach it (positive score)
            elif scaredTime > 0 and manhattan(newPos, ghostPos) < 2:
                score += 500  # approach scared ghosts
        return score

        #TODO get cpasules and evaluate them 

        # return successorGameState.getScore()


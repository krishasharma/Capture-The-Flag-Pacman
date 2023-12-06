from pacai.core import distance
from pacai.agents.capture.reflex import CaptureAgent

# from pacai.agents.capture.capture import CaptureAgent
# import random
# from pacai.core.directions import Directions

# TODO: do not import qulafied import THIS IS ONE OF THE CHECKS KAIA
# IDFK WHAT TO DO I WANNA CRYYYYYY
# TODO: make both agents offensive agents instead of defenisve offensive??
# TODO: implement getAction 
# TODO: implement getCapsule (getFood is a method we have access too)
# TODO: use getScore as a check to see how we're doing in the match; if we're doing really 
# well consider switching to full defense? else stick with offense? 

def createTeam(firstIndex, secondIndex, isRed,
        offensiveAgentONE = 'pacai.agents.capture.dummy.DummyAgent',
        offensiveAgnetTWO = 'pacai.agents.capture.dummy.DummyAgent'):
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
        # split the grid top and bottom; one agent handles top, one bottom
        offensiveAgentONE(firstIndex),
        offensiveAgentTWO(secondIndex),
    ]


class offensiveAgentONE(CaptureAgent):
    def __init__(self, index, offensive=True):
        super().__init__(index)
        self.offensive = offensive

    def chooseAction(self, gameState):
        legalMoves = gameState.getLegalActions(self.index)

        if self.offensive:
            return self.offensiveAction(gameState, legalMoves)
        else:
            return self.defensiveAction(gameState, legalMoves)

    def offensiveAction(self, gameState, legalMoves):
        # Sample offensive strategy: Seek food pellets and avoid ghosts.
        features = self.getFeatures(gameState)
        weights = self.getWeights(gameState)

        # Calculate a score for each action based on the features and weights.
        scores = {}
        for action in legalMoves:
            scores[action] = sum(features[feature] * weights[feature] for feature in features)

        # Choose the action with the highest score.
        bestAction = max(scores, key=scores.get)
        return bestAction

    def defensiveAction(self, gameState, legalMoves):
        # Sample defensive strategy: Protect the home base and chase invading opponents.
        features = self.getFeatures(gameState)
        weights = self.getWeights(gameState)

        # Calculate a score for each action based on the features and weights.
        scores = {}
        for action in legalMoves:
            scores[action] = sum(features[feature] * weights[feature] for feature in features)

        # Choose the action with the highest score.
        bestAction = max(scores, key=scores.get)
        return bestAction

    def getFeatures(self, gameState):
        features = {}

        if self.offensive:
            # Offensive features:
            myPos = gameState.getAgentPosition(self.index)
            foodList = self.getFood(gameState).asList()

            # Feature 1: Distance to the closest food pellet.
            if foodList:
                closestFoodDist = min(distance.manhattan(myPos, food) for food in foodList)
                features['closestFoodDist'] = closestFoodDist
            else:
                features['closestFoodDist'] = 0

            # Feature 2: Avoiding ghosts (negative score if close to ghosts).
            opponents = self.getOpponents(gameState)
            ghostStates = [gameState.getAgentState(ghost) for ghost in opponents]

            for ghostState in ghostStates:
                if not ghostState.isPacman:
                    ghostPos = ghostState.getPosition()
                    distToGhost = distance.manhattan(myPos, ghostPos)

                    if distToGhost <= 1:  # Dangerously close to a ghost.
                        features['avoidGhost'] = -1
                        break
            else:
                features['avoidGhost'] = 0  # No ghost nearby.

        else:
            # Defensive features:
            myPos = gameState.getAgentPosition(self.index)
            opponents = self.getOpponents(gameState)
            invaderStates = [gameState.getAgentState(invader) for invader in opponents if invader.isPacman]

            # Feature 1: Distance to the closest invader.
            if invaderStates:
                closestInvaderDist = min(distance.manhattan(myPos, invader.getPosition()) for invader in invaderStates)
                features['closestInvaderDist'] = closestInvaderDist
            else:
                features['closestInvaderDist'] = 0

            # Feature 2: Protecting the home base (negative score if opponents are nearby).
            for invaderState in invaderStates:
                invaderPos = invaderState.getPosition()
                distToInvader = distance.manhattan(myPos, invaderPos)

                if distToInvader <= 3:  # Close enough to an invader.
                    features['protectBase'] = -1
                    break
            else:
                features['protectBase'] = 0  # No invader nearby.

        return features

    def getWeights(self, gameState):
        weights = {}

        if self.offensive:
            # Offensive weights:
            weights['closestFoodDist'] = -1  # Try to get closer to food.
            weights['avoidGhost'] = -100  # Strongly avoid ghosts if they are nearby.

        else:
            # Defensive weights:
            weights['closestInvaderDist'] = -1  # Try to get closer to invaders.
            weights['protectBase'] = -100  # Strongly protect the base if invaders are nearby.

        return weights
    


class offensiveAgentTWO(CaptureAgent):
    def __init__(self, index, offensive=True):
        super().__init__(index)
        self.offensive = offensive

    def chooseAction(self, gameState):
        legalMoves = gameState.getLegalActions(self.index)

        if self.offensive:
            return self.offensiveAction(gameState, legalMoves)
        else:
            return self.defensiveAction(gameState, legalMoves)

    def offensiveAction(self, gameState, legalMoves):
        # Sample offensive strategy: Seek food pellets and avoid ghosts.
        features = self.getFeatures(gameState)
        weights = self.getWeights(gameState)

        # Calculate a score for each action based on the features and weights.
        scores = {}
        for action in legalMoves:
            scores[action] = sum(features[feature] * weights[feature] for feature in features)

        # Choose the action with the highest score.
        bestAction = max(scores, key=scores.get)
        return bestAction

    def defensiveAction(self, gameState, legalMoves):
        # Sample defensive strategy: Protect the home base and chase invading opponents.
        features = self.getFeatures(gameState)
        weights = self.getWeights(gameState)

        # Calculate a score for each action based on the features and weights.
        scores = {}
        for action in legalMoves:
            scores[action] = sum(features[feature] * weights[feature] for feature in features)

        # Choose the action with the highest score.
        bestAction = max(scores, key=scores.get)
        return bestAction

    def getFeatures(self, gameState):
        features = {}

        if self.offensive:
            # Offensive features:
            myPos = gameState.getAgentPosition(self.index)
            foodList = self.getFood(gameState).asList()

            # Feature 1: Distance to the closest food pellet.
            if foodList:
                closestFoodDist = min(distance.manhattan(myPos, food) for food in foodList)
                features['closestFoodDist'] = closestFoodDist
            else:
                features['closestFoodDist'] = 0

            # Feature 2: Avoiding ghosts (negative score if close to ghosts).
            opponents = self.getOpponents(gameState)
            ghostStates = [gameState.getAgentState(ghost) for ghost in opponents]

            for ghostState in ghostStates:
                if not ghostState.isPacman:
                    ghostPos = ghostState.getPosition()
                    distToGhost = distance.manhattan(myPos, ghostPos)

                    if distToGhost <= 1:  # Dangerously close to a ghost.
                        features['avoidGhost'] = -1
                        break
            else:
                features['avoidGhost'] = 0  # No ghost nearby.

        else:
            # Defensive features:
            myPos = gameState.getAgentPosition(self.index)
            opponents = self.getOpponents(gameState)
            invaderStates = [gameState.getAgentState(invader) for invader in opponents if invader.isPacman]

            # Feature 1: Distance to the closest invader.
            if invaderStates:
                closestInvaderDist = min(distance.manhattan(myPos, invader.getPosition()) for invader in invaderStates)
                features['closestInvaderDist'] = closestInvaderDist
            else:
                features['closestInvaderDist'] = 0

            # Feature 2: Protecting the home base (negative score if opponents are nearby).
            for invaderState in invaderStates:
                invaderPos = invaderState.getPosition()
                distToInvader = distance.manhattan(myPos, invaderPos)

                if distToInvader <= 3:  # Close enough to an invader.
                    features['protectBase'] = -1
                    break
            else:
                features['protectBase'] = 0  # No invader nearby.

        return features

    def getWeights(self, gameState):
        weights = {}

        if self.offensive:
            # Offensive weights:
            weights['closestFoodDist'] = -1  # Try to get closer to food.
            weights['avoidGhost'] = -100  # Strongly avoid ghosts if they are nearby.

        else:
            # Defensive weights:
            weights['closestInvaderDist'] = -1  # Try to get closer to invaders.
            weights['protectBase'] = -100  # Strongly protect the base if invaders are nearby.

        return weights
    

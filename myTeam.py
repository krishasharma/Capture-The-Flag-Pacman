# from pacai.util import reflection
from pacai.agents.capture.reflex import CaptureAgent
# import random
# from pacai.util import util
from pacai.core import distance

# TODO: do not import qulafied import THIS IS ONE OF THE CHECKS KAIA
# IDFK WHAT TO DO I WANNA CRYYYYYY
# TODO: make both agents offensive agents instead of defenisve offensive??
# Mario test
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
        # split the grid top and bottom; one agent handles top, one bottom
        offensiveAgentTOP(firstIndex),
        offensiveAgentBOTTOM(secondIndex),
    ]

# reflex capture agent ???
# TODO: change this to match the offensive agent? (only if we wanna have two offensive agents)
# agent for top
class offensiveAgentTOP(CaptureAgent):
    def getFeatures(self, gameState, action):
        features = {}
        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        # actions = self.getAction(gameState)

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
    

# reflex capture agent ???
# agent for bottom of grid
class offensiveAgentBOTTOM(CaptureAgent):
    def getFeatures(self, gameState, action):
        features = {}
        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        # actions = self.getAction(gameState)

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

    def DecisiveAction(self, gameState):

        actions = self.getAction(gameState)
        

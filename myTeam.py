# from pacai.util import reflection
from pacai.agents.capture.reflex import CaptureAgent
import random
# from pacai.util import util

# TODO: do not import qulafied import THIS IS ONE OF THE CHECKS KAIA

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

class defensiveAgent(CaptureAgent): # defensive
    """
    A dummy agent that takes random actions.
    """
    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
        self.index = index

    def chooseAction(self, gameState):
        legalActions = gameState.getLegalActions(self.index)
        return random.choice(legalActions)

    def registerInitialState(self, gameState):
        """
        This method handles the initial setup of the agent and populates useful fields,
        such as the team the agent is on and the `pacai.core.distanceCalculator.Distancer`.

        IMPORTANT: If this method runs for more than 15 seconds, your agent will time out.
        """

        super().registerInitialState(gameState)

class offensiveAgent(CaptureAgent): # offensive
    """
    A dummy defensive agent that takes random actions.
    """
    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
        self.index = index

    def chooseAction(self, gameState):
        legalActions = gameState.getLegalActions(self.index)
        return random.choice(legalActions)

    def registerInitialState(self, gameState):
        """
        This method handles the initial setup of the agent and populates useful fields,
        such as the team the agent is on and the `pacai.core.distanceCalculator.Distancer`.

        IMPORTANT: If this method runs for more than 15 seconds, your agent will time out.
        """

        super().registerInitialState(gameState)



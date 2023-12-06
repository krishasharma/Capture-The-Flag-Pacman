from pacai.core import distance
from pacai.agents.capture.reflex import CaptureAgent
from pacai.util import util
from pacai.agents.capture.reflex import ReflexCaptureAgent
# from pacai.agents.capture.capture import CaptureAgent
import random
# from pacai.core.directions import Directions

# TODO: do not import qulafied import THIS IS ONE OF THE CHECKS KAIA
# IDFK WHAT TO DO I WANNA CRYYYYYY
# TODO: make both agents offensive agents instead of defenisve offensive??
# TODO: implement getAction 
# TODO: implement getCapsule (getFood is a method we have access too)
# TODO: use getScore as a check to see how we're doing in the match; if we're doing really 
# well consider switching to full defense? else stick with offense? 


# TODO: consider that maybe the agents have no incentive to go out and get the food
# right now both agents linger in the corner

def createTeam(firstIndex, secondIndex, isRed,
        first = 'OffensiveReflexAgent',
        second = 'DefensiveReflexAgent'):
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
        OffensiveReflexAgent(firstIndex),
        DefensiveReflexAgent(secondIndex),
    ]

class BaseReflexAgent(ReflexCaptureAgent):
    def isGhostNearby(self, gameState, dangerDistance):
        """
        Check if any ghost is within the dangerDistance.
        """
        myPos = gameState.getAgentPosition(self.index)
        opponents = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
        for opponent in opponents:
            if not opponent.isPacman and opponent.getPosition() is not None:
                if self.getMazeDistance(myPos, opponent.getPosition()) < dangerDistance:
                    return True
        return False

    def isOnEnemySide(self, gameState, position=None):
        """
        Check if the agent or a given position is on the enemy's side of the map.
        """
        if position is None:
            position = gameState.getAgentPosition(self.index)

        isRedTeam = gameState.isOnRedTeam(self.index)
        if isRedTeam:
            return not gameState.isOnRedSide(position)
        else:
            return gameState.isOnRedSide(position)
        

class OffensiveReflexAgent(BaseReflexAgent):
    def chooseAction(self, gameState):
        # Switch to defense if an enemy Pacman is detected on our side
        if self.isEnemyPacmanOnOurSide(gameState):
            return self.defensiveAction(gameState)

        # Otherwise, continue with offensive behavior
        if self.isGhostNearby(gameState, dangerDistance=3) and self.isOnEnemySide(gameState):
            return self.fleeAction(gameState)
        else:
            return self.collectFoodAction(gameState)

    def isEnemyPacmanOnOurSide(self, gameState):
        """
        Check if there is any enemy Pacman on our side of the map.
        """
        enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
        for enemy in enemies:
            if enemy.isPacman and not self.isOnEnemySide(gameState, enemy.getPosition()):
                return True
        return False
    
    def defensiveAction(self, gameState):
        """
        Implement a defensive strategy involving ambushing or coordinating.
        """
        enemyPacmen = self.getEnemyPacmen(gameState)
        if enemyPacmen:
            target = self.chooseAmbushTarget(gameState, enemyPacmen)
            return self.moveToPosition(gameState, target)
        else:
            # If no enemy is on our side, return to a default defensive position
            return self.moveToPosition(gameState, self.getDefaultDefensivePosition(gameState))

    def getEnemyPacmen(self, gameState):
        """
        Get a list of enemy Pacmen on our side of the map.
        """
        enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
        return [enemy for enemy in enemies if enemy.isPacman and not self.isOnEnemySide(gameState, enemy.getPosition())]

    def chooseAmbushTarget(self, gameState, enemyPacmen):
        """
        Choose an ambush target based on the predicted path of enemy Pacmen.
        """
        # Implement logic to predict the enemy's path or choose a strategic chokepoint
        # Example: return the position of the nearest food to the enemy Pacman
        myPos = gameState.getAgentPosition(self.index)
        return min((self.getMazeDistance(myPos, pacman.getPosition()), pacman.getPosition()) for pacman in enemyPacmen)[1]

    def moveToPosition(self, gameState, targetPosition):
        """
        Move towards the given target position.
        """
        bestAction = None
        bestDistance = float('inf')
        myPos = gameState.getAgentPosition(self.index)

        for action in gameState.getLegalActions(self.index):
            successor = self.getSuccessor(gameState, action)
            newPos = successor.getAgentPosition(self.index)
            distance = self.getMazeDistance(newPos, targetPosition)

            if distance < bestDistance:
                bestDistance = distance
                bestAction = action

        return bestAction
    
    def collectFoodAction(self, gameState):
        # Prioritize food that is furthest away to maximize territory coverage
        foodList = self.getFood(gameState).asList()
        bestDistance = float('inf')
        bestAction = None
        myPos = gameState.getAgentPosition(self.index)

        for action in gameState.getLegalActions(self.index):
            successor = self.getSuccessor(gameState, action)
            newPos = successor.getAgentPosition(self.index)
            minDistance = min([self.getMazeDistance(newPos, food) for food in foodList])
            if minDistance < bestDistance:
                bestDistance = minDistance
                bestAction = action

        return bestAction

    def fleeAction(self, gameState):
        # Choose an action that increases the distance from the nearest ghost
        bestDistance = 0
        bestAction = None
        myPos = gameState.getAgentPosition(self.index)

        for action in gameState.getLegalActions(self.index):
            successor = self.getSuccessor(gameState, action)
            newPos = successor.getAgentPosition(self.index)
            nearestGhostDistance = min([self.getMazeDistance(newPos, opp.getPosition()) 
                                        for opp in self.getOpponents(gameState)
                                        if gameState.getAgentState(opp).getPosition() is not None and
                                        not gameState.getAgentState(opp).isPacman])

            if nearestGhostDistance > bestDistance:
                bestDistance = nearestGhostDistance
                bestAction = action

        return bestAction if bestAction is not None else random.choice(gameState.getLegalActions(self.index))
    

class DefensiveReflexAgent(BaseReflexAgent):
    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
        self.initialPositionSet = False

    def chooseAction(self, gameState):
        # Initially move to a central position
        if not self.initialPositionSet:
            self.initialPosition = self.getCentralPosition(gameState)
            self.initialPositionSet = True

        if self.isEnemyPacmanOnOurSide(gameState):
            # Switch to active defense if an enemy crosses into our side
            return self.huntEnemyPacmanAction(gameState)
        else:
            # Stay around the central position to maintain a proactive defense
            return self.moveToPosition(gameState, self.initialPosition)

    LAYOUT_WIDTH = None
    LAYOUT_HEIGHT = None

    def registerInitialState(self, gameState):
        super().registerInitialState(gameState)
        if DefensiveReflexAgent.LAYOUT_WIDTH is None or DefensiveReflexAgent.LAYOUT_HEIGHT is None:
            foodGrid = gameState.getBlueFood()  # or gameState.getRedFood()
            DefensiveReflexAgent.LAYOUT_WIDTH = foodGrid.getWidth()
            DefensiveReflexAgent.LAYOUT_HEIGHT = foodGrid.getHeight()

        self.initialPosition = self.getCentralPosition(gameState)
        self.initialPositionSet = True

    def getCentralPosition(self, gameState):
        centralX = DefensiveReflexAgent.LAYOUT_WIDTH // 2
        centralY = DefensiveReflexAgent.LAYOUT_HEIGHT // 2

        # Adjust for red team
        if gameState.isOnRedTeam(self.index):
            centralX -= 1

        # Ensure the central position is not a wall
        while gameState.hasWall(centralX, centralY):
            centralY -= 1

        return (centralX, centralY)
    
    def isEnemyPacmanOnOurSide(self, gameState):
        """
        Check if there is any enemy Pacman on our side of the map.
        """
        enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
        for enemy in enemies:
            if enemy.isPacman and not self.isOnEnemySide(gameState, enemy.getPosition()):
                return True
        return False
    
    def huntEnemyPacmanAction(self, gameState):
        # Target the nearest visible enemy Pacman
        bestDistance = float('inf')
        bestAction = None
        myPos = gameState.getAgentPosition(self.index)
        enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
        pacmen = [enemy for enemy in enemies if enemy.isPacman and enemy.getPosition() is not None]

        if not pacmen:
            return random.choice(gameState.getLegalActions(self.index))

        for action in gameState.getLegalActions(self.index):
            successor = self.getSuccessor(gameState, action)
            newPos = successor.getAgentPosition(self.index)
            distanceToNearestPacman = min([self.getMazeDistance(newPos, pacman.getPosition()) for pacman in pacmen])

            if distanceToNearestPacman < bestDistance:
                bestDistance = distanceToNearestPacman
                bestAction = action

        return bestAction
    
    def moveToPosition(self, gameState, targetPosition):
        """
        Move towards the given target position.
        """
        bestAction = None
        bestDistance = float('inf')
        myPos = gameState.getAgentPosition(self.index)

        for action in gameState.getLegalActions(self.index):
            successor = self.getSuccessor(gameState, action)
            newPos = successor.getAgentPosition(self.index)
            distance = self.getMazeDistance(newPos, targetPosition)

            if distance < bestDistance:
                bestDistance = distance
                bestAction = action

        return bestAction
    
    def returnToDefenseAction(self, gameState):
        # Return to a defensive position on the home side
        bestDistance = float('inf')
        bestAction = None
        myPos = gameState.getAgentPosition(self.index)
        defensivePosition = self.getDefensivePosition(gameState)

        for action in gameState.getLegalActions(self.index):
            successor = self.getSuccessor(gameState, action)
            newPos = successor.getAgentPosition(self.index)
            distanceToPosition = self.getMazeDistance(newPos, defensivePosition)

            if distanceToPosition < bestDistance:
                bestDistance = distanceToPosition
                bestAction = action

        return bestAction

    def getDefensivePosition(self, gameState):
        """
        Determine a strategic defensive position based on the distribution of remaining food.
        """
        foodList = self.getFoodYouAreDefending(gameState).asList()
        if not foodList:
            # No food left to defend, choose a default position
            return self.getDefaultDefensivePosition(gameState)

        # Calculate the centroid of the remaining food
        x = [food[0] for food in foodList]
        y = [food[1] for food in foodList]
        centroid = (sum(x) / len(foodList), sum(y) / len(foodList))

        # Find the nearest legal position to the centroid
        return self.getNearestLegalPosition(gameState, centroid)

    def getDefaultDefensivePosition(self, gameState):
        """
        Get a default defensive position (e.g., near the center of your side).
        """
        layout = gameState.getLayout()
        midpointX = layout.getWidth() // 2
        midpointY = layout.getHeight() // 2
        if not gameState.isOnRedTeam(self.index):
            midpointX -= 1  # Adjust for blue team

        return (midpointX, midpointY)

    def getNearestLegalPosition(self, gameState, position):
        """
        Find the nearest legal position to the given position.
        """
        layout = gameState.getLayout()
        x, y = int(position[0]), int(position[1])
        if layout.isWall((x, y)):
            # Find the nearest non-wall position
            return self.findClosestNonWall(gameState, x, y)
        return (x, y)

    def findClosestNonWall(self, gameState, x, y):
        """
        Find the closest non-wall position to the given coordinates.
        """
        layout = gameState.getLayout()
        for dx, dy in itertools.product(range(-1, 2), repeat=2):
            if not layout.isWall((x + dx, y + dy)):
                return (x + dx, y + dy)
        return (x, y)  # Return the original position if all nearby are walls
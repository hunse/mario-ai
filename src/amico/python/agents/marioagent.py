__author__="Sergey Karakovskiy, sergey at idsia fullstop ch"
__date__ ="$May 2, 2009 7:54:12 PM$"

import numpy as np


class MarioAgent(object):
    """ An agent is an entity capable of producing actions, based on previous observations.
        Generally it will also learn from experience. It can interact directly with a Task.
    """

    class Action(object):
        order = ['left', 'right', 'down', 'jump', 'run', 'up']

        def __init__(self, value=False):
            for param in self.order:
                setattr(self, param, value)

        def as_tuple(self):
            return tuple(map(int, [getattr(self, p) for p in self.order]))


    _name = None

    scene = None
    enemies = None
    mayMarioJump = None
    isMarioOnGround = None
    marioFloats = None
    enemiesFloats = None
    marioState = None

    isEpisodeOver = False

    @property
    def name(self):
        if self._name is None:
            self._name = self.__class__.__name__
        return self._name

    @name.setter
    def name(self, newname):
        """Change name to newname. Uniqueness is not guaranteed anymore."""
        self._name = newname

    def __repr__(self):
        """ The default representation of a named object is its name. """
        return "<%s '%s'>" % (self.__class__.__name__, self.name)

    def setObservationDetails(self, rfWidth, rfHeight, egoRow, egoCol):
        rfShape = (rfHeight, rfWidth)
        self.scene = np.zeros(rfShape)
        self.enemies = np.zeros(rfShape)
        self.marioEgoRow = egoRow
        self.marioEgoCol = egoCol

    def integrateObservation(self, flatScene, flatEnemies, marioPos, enemiesPos, marioState):
        """This method stores the observation inside the agent"""
        self.scene.reshape(-1)[:] = flatScene
        self.enemies.reshape(-1)[:] = flatEnemies

        self.marioFloats = marioPos
        self.enemiesFloats = enemiesPos
        self.mayMarioJump = marioState[3]
        self.isMarioOnGround = marioState[2]
        self.marioState = marioState[1]
        self.printScene()
        # raw_input("Pause:")

    def printScenePoint(self, i, j):
        def elToStr(i):
            return {
                0: " ", -60: "-", -85: "P",  # empty, ground, pipe
                -24: "B", 2: "*", -62: "^"  # block, coin, platform
            }.get(i, str(i))

        def enToStr(i):
            return {
                0: " ", 80: "G",  # empty, goomba
            }.get(i, str(i))

        if i == self.marioEgoRow and j == self.marioEgoCol:
            s = "M"
        elif self.enemies[i, j] != 0:
            s = enToStr(self.enemies[i, j])
        elif self.scene[i, j] != 0:
            s = elToStr(self.scene[i, j])
        else:
            s = " "
        return s + " "

    def printScene(self):
        rows = []
        for i in range(self.scene.shape[0]):
            row = ""
            for j in range(self.scene.shape[1]):
                row += self.printScenePoint(i, j)
            rows.append(row)
        print "\n".join(rows)

    def newEpisode(self):
        pass

    def giveIntermediateReward(self, reward):
        pass

    def getAction(self):
        """Choose the agent's current action.

        Returns
        -------
        action : tuple
            A tuple of binary values (as 0 or 1) representing the action.
        """
        raise NotImplementedError("Agent must implement getAction()")

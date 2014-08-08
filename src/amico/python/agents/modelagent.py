# -*- coding: utf-8 -*-
__author__ = "Sergey Karakovskiy, sergey at idsia fullstop ch"
__date__ = "$May 1, 2009 2:46:34 AM$"

from marioagent import MarioAgent


class ModelAgent(MarioAgent):
    """An agent demonstrating how to use the MarioAgent base class
    and Simulator object.

    Adapted from forwardagent.py.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        self.isEpisodeOver = False
        self.trueJumpCounter = 0
        self.trueSpeedCounter = 0
        self.action = self.Action()

    def getCellValue(self, i, j, ego=True):
        if ego:
            i = i + self.marioEgoRow
            j = j + self.marioEgoCol

        if (i < 0 or i >= self.scene.shape[0] or
            j < 0 or j >= self.scene.shape[1]):
            return 0
        elif self.enemies[i, j] != 0:
            return self.enemies[i, j]
        else:
            return self.scene[i, j]

    def getAction(self):
        """ Possible analysis of current observation and sending an action back
        """
        if self.isEpisodeOver:
            return self.Action(True).as_tuple()

        self.action.right = 1
        # self.action.run = 1

        if (self.getCellValue(0, 1) != 0 or self.getCellValue(0, 2) != 0):
            if (self.mayMarioJump or \
                (not self.isMarioOnGround and self.action.jump)):
                self.action.jump = 1
            self.trueJumpCounter += 1
        else:
            self.action.jump = 0
            self.trueJumpCounter = 0

        if (self.trueJumpCounter > 16):
            self.trueJumpCounter = 0
            self.action.jump = 0

        return self.action.as_tuple()


if __name__ == '__main__':
    from simulator import Simulator

    agent = ModelAgent()
    sim = Simulator(agent, visualize=True)
    info = sim.run_level(seed=0)
    print info

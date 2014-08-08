# -*- coding: utf-8 -*-
__author__ = "Sergey Karakovskiy, sergey at idsia fullstop ch"
__date__ = "$May 1, 2009 2:46:34 AM$"

from marioagent import MarioAgent

class ForwardAgent(MarioAgent):
    """ In fact the Python twin of the
        corresponding Java ForwardAgent.
    """
    action = None
    actionStr = None
    KEY_JUMP = 3
    KEY_SPEED = 4
    levelScene = None
    mayMarioJump = None
    isMarioOnGround = None
    marioFloats = None
    enemiesFloats = None
    isEpisodeOver = False
    marioState = None

    trueJumpCounter = 0;
    trueSpeedCounter = 0;

    """default values for observation details"""
    receptiveFieldWidth = 19
    receptiveFieldHeight = 19
    marioEgoRow = 9
    marioEgoCol = 9

    agentName = "AmiCo Python Forward Agent"


    def reset(self):
        self.isEpisodeOver = False
        self.trueJumpCounter = 0;
        self.trueSpeedCounter = 0;

    def __init__(self):
        """Constructor"""
        self.trueJumpCounter = 0
        self.trueSpeedCounter = 0
        self.action = [0, 0, 0, 0, 0, 0]
        self.action[1] = 1
        self.actionStr = ""
        self.agentName = "Python Forward Agent"

    def getReceptiveFieldCellValue(self, i, j):
        if (i < 0 or i >= self.receptiveFieldHeight or
            j < 0 or j >= self.receptiveFieldWidth):
            return 0
        return self.levelScene[i][j]

    def setObservationDetails(self, rfWidth, rfHeight, egoRow, egoCol):
        self.receptiveFieldWidth = rfWidth
        self.receptiveFieldHeight = rfHeight
        self.marioEgoRow = egoRow
        self.marioEgoCol = egoCol

    def giveIntermediateReward(self, reward):
        pass

    def getAction(self):
        """ Possible analysis of current observation and sending an action back
        """
    	if (self.isEpisodeOver):
    	    return (1, 1, 1, 1, 1, 1)

        if (self.getReceptiveFieldCellValue(self.marioEgoRow, self.marioEgoCol + 2) != 0 or \
            self.getReceptiveFieldCellValue(self.marioEgoRow, self.marioEgoCol + 1) != 0):
            # print "entered getAction2"
            if (self.mayMarioJump or \
                (not self.isMarioOnGround and self.action[self.KEY_JUMP] == 1)):
                #print "entered getAction3"
                self.action[self.KEY_JUMP] = 1
            #print "entered getAction4"
            self.trueJumpCounter += 1
        else:
            # print "entered getAction5"
            self.action[self.KEY_JUMP] = 0;
            self.trueJumpCounter = 0
        # print "entered getAction6"
        if (self.trueJumpCounter > 16):
            self.trueJumpCounter = 0
            self.action[self.KEY_JUMP] = 0;

        # self.action[self.KEY_SPEED] = danger
        return tuple(self.action)

    def getName(self):
        return self.agentName

    def integrateObservation(self, squashedObservation, squashedEnemies, marioPos, enemiesPos, marioState):
        """This method stores the observation inside the agent"""
        #print "Py: got observation::: squashedObservation: \n", squashedObservation
        #print "Py: got observation::: squashedEnemies: \n", squashedEnemies
        #print "Py: got observation::: marioPos: \n", marioPos
        #print "Py: got observation::: enemiesPos: \n", enemiesPos
        #print "Py: got observation::: marioState: \n", marioState

        row = self.receptiveFieldHeight
        col = self.receptiveFieldWidth
        levelScene=[]
        enemiesObservation=[]

        for i in range(row):
            levelScene.append(squashedObservation[i*col:i*col+col])

        for i in range(row):
            enemiesObservation.append(squashedEnemies[i*col:i*col+col])

        self.marioFloats = marioPos
        self.enemiesFloats = enemiesPos
        self.mayMarioJump = marioState[3]
        self.isMarioOnGround = marioState[2]
        self.marioState = marioState[1]
        self.levelScene = levelScene
        #self.printLevelScene()

    def printLevelScene(self):
        ret = ""
        for x in range(self.receptiveFieldWidth):
            tmpData = ""
            for y in range(self.receptiveFieldHeight):
                tmpData += self.mapElToStr(self.getReceptiveFieldCellValue(x, y));
            ret += "\n%s" % tmpData;
        print ret

    def mapElToStr(self, el):
        """maps element of levelScene to str representation"""
        s = "";
        if  (el == 0):
            s = "##"
        s += "#MM#" if (el == 95) else str(el)
        while (len(s) < 4):
            s += "#";
        return s + " "

    def printObs(self):
        """for debug"""
        print repr(self.observation)


if __name__ == '__main__':
    from simulator import Simulator

    agent = ForwardAgent()
    sim = Simulator(agent, visualize=False)
    info = sim.run_level(seed=0)
    print info

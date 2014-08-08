import sys
import os

import ctypes
from ctypes import *
from ctypes import POINTER
from ctypes import c_int
from ctypes import py_object
from ctypes.util import find_library

import numpy as np

from evaluationinfo import EvaluationInfo


class ListPOINTER(object):
    '''Just like a POINTER but accept a list of ctype as an argument'''
    def __init__(self, etype):
        self.etype = etype

    def from_param(self, param):
        if isinstance(param, (list, tuple)):
#            print "Py: IS INSTANCE"
            return (self.etype * len(param))(*param)
        else:
#            print "Py: NOT INSTANCE"
            return param


class ListByRef(object):
    '''An argument that converts a list/tuple of ctype elements
    into a pointer to an array of pointers to the elements'''
    def __init__(self, etype):
        self.etype = etype
        self.etype_p = POINTER(etype)

    def from_param(self, param):
        if isinstance(param, (list, tuple)):
            val = (self.etype_p * len(param))()
            for i, v in enumerate(param):
                if isinstance(v, self.etype):
                    val[i] = self.etype_p(v)
                else:
                    val[i] = v
            return val
        else:
            return param


def from_param(self, param):
    if isinstance(param, (list, tuple)):
        return (self.etype * len(param))(*param)
    else:
        return param


def cfunc(name, dll, result, * args):
    '''build and apply a ctypes prototype complete with parameter flags'''
    atypes = []
    aflags = []
    for arg in args:
        atypes.append(arg[1])
        aflags.append((arg[2], arg[0]) + arg[3:])
    return CFUNCTYPE(result, * atypes)((name, dll), tuple(aflags))


class Simulator(object):

    def __init__(self, agent, visualize=False):
        self.agent = agent

        options = "-vis %s" % ("on" if visualize else "off")
        # options += "
        self.options = options

        # --- load libAmiCoPyJava.so
        print "Py: AmiCo Simulation Started:"
        print "library found: "
        print "Platform: ", sys.platform
        if (sys.platform == 'linux2'):
            ##########################################
            # find_library on Linux could only be used if your libAmiCoPyJava.so is
            # on system search path or path to the library is added in to LD_LIBRARY_PATH
            #
            # name =  'AmiCoPyJava'
            # loadName = find_library(name)
            ##########################################
            loadName = './libAmiCoPyJava.so'
            libamico = ctypes.CDLL(loadName)
            print libamico
        else: #else if OS is a Mac OS X (libAmiCo.dylib is searched for) or Windows (AmiCo.dll)
            name =  'AmiCoPyJava'
            loadName = find_library(name)
            print loadName
            libamico = ctypes.CDLL(loadName)
            print libamico

        javaClass = "ch/idsia/benchmark/mario/environments/MarioEnvironment"
        libamico.amicoInitialize(1, "-Djava.class.path=." + os.pathsep + ":jdom.jar")
        libamico.createMarioEnvironment(javaClass)
        self.libamico = libamico

        self.reset = cfunc(
            'reset', libamico, None, ('list', ListPOINTER(c_int), 1))
        self.getEntireObservation = cfunc(
            'getEntireObservation', libamico, py_object,
            ('list', c_int, 1), ('zEnemies', c_int, 1))
        self.performAction = cfunc(
            'performAction', libamico, None, ('list', ListPOINTER(c_int), 1))
        self.getEvaluationInfo = cfunc(
            'getEvaluationInfo', libamico, py_object)
        self.getObservationDetails = cfunc(
            'getObservationDetails', libamico, py_object)

    def run_level(self, seed=None):
        if seed is None:
            seed = np.random.randint(2**31 - 1)

        options1 = self.options + (" -ls %d" % seed)
        print "options: ", options1

        self.reset(options1)
        obsDetails = self.getObservationDetails()
        self.agent.setObservationDetails(
            obsDetails[0], obsDetails[1], obsDetails[2], obsDetails[3])

        levelIterations = 0
        while (not self.libamico.isLevelFinished()):
            levelIterations +=1
            self.libamico.tick();
            obs = self.getEntireObservation(1, 0)
            self.agent.integrateObservation(obs[0], obs[1], obs[2], obs[3], obs[4])
            action = self.agent.getAction()
            #print "action: ", action
            self.performAction(action)

        print "Py: LEVEL ITERATIONS: ", levelIterations
        evaluationInfo = self.getEvaluationInfo()
        return EvaluationInfo(evaluationInfo)

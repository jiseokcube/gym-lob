import gym
from gym import spaces
from gym.utils import seeding

import numpy as np
import ctypes as C

def openLOB(filename):
    with open(filename) as file:
        reader = csv.reader(ifile, delimiter=',')
        data = []
        for row in reader:
            data += row

    libc = C.CDLL('msvcrt')
    libc.malloc.restype = C.POINTER(C.c_double)
    p_data = libc.malloc(len(data) * C.sizeof(C.c_double))
    pointer = C.cast(p_data, C.POINTER(C.c_double * len(data)))
    array = np.asarray(pointer.contents)
    array[:] = np.array(data)
    return p_data

def closeLOB(pointer):
    libc = C.CDLL('msvcrt')
    libc.free(pointer)

class LOBEnv(gym.Env):
    lobs = None
    lengths = None

    def __init__(self, days=None):
        if LOBEnv.lobs is None and days is not None:
            LOBEnv.lobs = [None] * days
            LOBEnv.lengths = [None] * days
        self.observation_space = spaces.Box(low=0, high=500, shape=(20, 1), dtype=np.float64)
        self.action_space = spaces.Discrete(3)

        self.seed()
        self.reset()

    def step(self, action):
        ###

    def reset(self):
        self.shares = 0
        self.day = self.np_random.randint(len(LOBEnv.lobs))
        self.index = self.np_random.randint(LOBEnv.lengths[self.day])
        return self._get_obs()

    def close(self):
        for lob in LOBEnv.lobs:
            if lob is not None:
                closeLOB(lob)

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _get_obs(self):
        return LOBEnv.lobs[self.day][self.index : self.index + 20]

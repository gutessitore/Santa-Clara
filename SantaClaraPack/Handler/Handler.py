#!/usr/bin/env python

from pathos.pools import ProcessPool
import pathos as ph
from Config.Config import Config

class Handler(object):

    def __init__(self):
        self.config = Config().config
        pass

    def execute_pool(self, function, values: list):
        pool = ProcessPool(ncpus=ph.multiprocessing.cpu_count())
        resultados = pool.map(function, values)





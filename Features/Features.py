import numpy as np
import matplotlib.pyplot as plt
class Features(object):

    def __init__(self):
        pass

    def derivative(self, data):

        dx = np.gradient(data)
        d2x = np.gradient(dx)

        return dx, d2x

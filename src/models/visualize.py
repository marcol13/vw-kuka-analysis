import matplotlib.pyplot as plt
import pandas as pd

class Visualize:
    def __init__(self, data, title):
        self.data = data
        self.title = title

    def plot(self):
        plt.plot(self.data)
        plt.title(self.title)
        plt.legend(self.data.columns)
        plt.show()

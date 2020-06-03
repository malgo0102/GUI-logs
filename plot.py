import matplotlib.pyplot as plt

class Plot:
    def __init__(self, model):
        self.model = model

    def show(self, column, columnName):
        """Show a plot with "Some numbers" column"""
        plt.plot(column, "ro")
        plt.ylabel(columnName)
        plt.show()

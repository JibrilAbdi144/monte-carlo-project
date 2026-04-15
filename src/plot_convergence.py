import matplotlib.pyplot as plt
import numpy as np

def plotConvergenceGraph(pathway_counts: list, relative_errors):
    '''
    Plots the relative error of the Monte-Carlo option prices against the number of simulation pathways generated.

    Arguments:
        pathway_counts (list): The list of the number of simulation pathway numbers to be analysed.
        relative_errors (np.ndarray): The relative errors that correspond to each simulation pathway number.

    Returns:
        None
    '''

    #Initialises the figure and axes objects
    figure, axes = plt.subplots()

    #Plots both a log-log plot of the relative errors against the number of simulation pathways and also plots the Central Limmit Theorem theoretical line
    axes.loglog(pathway_counts, relative_errors, "o-", label="Monte-Carlo Relative Errors")
    axes.loglog(pathway_counts, [(relative_errors[0] / (pathway_counts[0] ** (-0.5))) * pathway_count ** (-0.5) for pathway_count in pathway_counts], "-", label=r"Central Limit Theorem Rate")

    #Sets the axes labels and the plot title
    axes.set_xlabel(r'Number of Simulations')
    axes.set_ylabel(r'Relative Error')
    axes.set_title("Monte-Carlo Convergence Analysis")

    #Shows the legend and the plot
    axes.legend(loc="upper right", fontsize=12, frameon=True, shadow=False)
    plt.show()
import matplotlib.pyplot as plt
import numpy as np

def plotConvergenceGraph(pathway_counts, dependent_variable):

    a, b = np.polyfit(np.log(pathway_counts), np.log(dependent_variable), 1)
    R = np.corrcoef(np.log(pathway_counts), np.log(dependent_variable))[0,1]

    figure, axes = plt.subplots()

    axes.loglog(pathway_counts, dependent_variable, "o-", label="Variance-Reduced Simulation Data")
    axes.loglog(pathway_counts, [np.exp(b) * pathway_count ** a for pathway_count in pathway_counts], "-", label=r"Best-Fit Plot")

    axes.set_xlabel(r'Number of Simulations')
    axes.set_ylabel(r'Relative Error')
    axes.set_title("Monte-Carlo Convergence Analysis")

    axes.legend(loc="upper right", fontsize=12, frameon=True, shadow=False)

    new_line = '\n'
    annotation_text = rf'$y={a:.2f}x+{b:.2f}${new_line}$R={R:.2f}$'
    axes.text(0.05, 0.05, annotation_text, transform=axes.transAxes, fontsize=12,
              horizontalalignment="left", verticalalignment="bottom",
              bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))

    
    plt.show()